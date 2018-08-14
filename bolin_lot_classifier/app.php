<?php
ini_set('display_errors', 'On');
error_reporting(1);
date_default_timezone_set("America/Chicago");

require 'vendor/autoload.php';
require 'debug.php';
//require 'camera_functions.php';

$app = new \Slim\App(['displayErrorDetails' => true]);

//pdo sucks 
$db = new mysqli("localhost", "p-lot",'horseblanketdonkey', "p-lot");

// Get a reference to the slim container so we can add to it.
$container = $app->getContainer();

$container['pdo'] = function ($container) {
    global $settings;
    $dsn = 'mysql:host=localhost;dbname=p-lot;charset=utf8';
    $usr = 'p-lot';
    $pwd = 'horseblanketdonkey';

    $pdo = new \Slim\PDO\Database($dsn, $usr, $pwd);
    return $pdo;
};

/****************************************************************************************************
 * ROUTES
 ****************************************************************************************************/

// GET /////////////////////////////////////////////////////////////////////////////////////
$app->get("/", "base");
$app->get("/example", "example_handler");
$app->get("/lot_image", "lot_image");
$app->get("/lot_overlay/{lot_id}/{image_id}", "lot_overlay");
$app->get("/lot[/{id}[/{json}]]", "lot");
$app->get("/camera", "camera");
$app->get("/trigger_camera", "trigger_camera");
$app->get("/weather", "weather");
$app->get("/image_number", "image_number");

// POST /////////////////////////////////////////////////////////////////////////////////////
$app->post("/image", "post_image");
$app->post("/example", "example_handler");
$app->post("/lock_image/{lot_id}/{image_id}/{lock}", "lock_image");
$app->post("/save/{lot_id}/{image_id}", "save_lot_image");

$app->run();

/****************************************************************************************************
 * CONTROLLERS
 ****************************************************************************************************/

/**
 * @Description: Shows all routes
 * @Example: curl -X GET https://griffincomplaints.xyz
 */
function base($request, $response, $args)
{
    global $app;
    $base_url = 'http://' . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'];

    $routes = $app->getContainer()->get('router')->getRoutes();
    $route_list = [];

    foreach ($routes as $key => $route) {
        $method = $route->getMethods();
        $pattern = $route->getPattern();
        $pattern = substr($pattern, 1);
        $route_list[$method[0]][] = $base_url . $pattern;

    }
    return json_response($response, 200, $route_list);
}

/**
 * @Params:
 *     $request (object): request type
 *     $response (object): response type
 *     $args (object): get args
 */
function weather($request, $response, $args)
{
    //debug (print_r($request->getParsedBody(),true), date('Y-m-d H:i:s').": get_image ", "./logs/output.log");

    $data['weather_data'] = _weather();
    $data['type'] = 'Get';
    $data['qparams'] = $request->getQueryParams();
    $data['params'] = $request->getParams();

    return json_response($response, 200, $data);
}

/**
 * Private weather function for internal use. Sends back data without all the response stuff added.
 * @Params:
 *     $request (object): request type
 *     $response (object): response type
 *     $args (object): get args
 */
function _weather()
{
    //debug (print_r($request->getParsedBody(),true), date('Y-m-d H:i:s').": get_image ", "./logs/output.log");

    $weather = file_get_contents("http://api.openweathermap.org/data/2.5/weather?zip=76308&appid=7121f0abc97aacff5b6044b0970718e0");
    if ($weather) {
        $weather = json_decode($weather);
    } else {
        $weather = false;
        debug("failed to get weather", date('Y-m-d H:i:s') . ": weather ", "./logs/output.log");
    }
    return $weather;
}

/**
 * lot: locks an image for editing
 * @getParams:
 *      lot_id=[int]      
 *      image_id=[int] 
 *      lock=[0,1]         
 * @usage:
 */
function lot($request, $response, $args)
{
    global $app;
    global $db;

    $allowed_params = [
        'id' => ['type'=>'int'],
        'json' => []
    ];

    $error = _check_params($allowed_params, $args);

    if(sizeof($error)>0){
        json_response($response, 200, $error);
    }

    if($args['id']){
        $lot_id = $args['id'];
    }else{
        $error = ['error'=>"No lot ID present! lot id must exist as a param."];
    }

    
    $sql = "SELECT lot_definition FROM `parking_lots` WHERE `id` = {$lot_id}";
    $result = $db->query($sql);
    if($result)
        $row = $result->fetch_assoc();
    $data = ['args' => $args, 'json'=>$row['lot_definition'],'error' => $error,'sql'=>$sql];

    return json_response($response, 200, $data);
}


/**
 * lock_image: locks an image for editing
 * @getParams:
 *      lot_id=[int]      
 *      image_id=[int] 
 *      lock=[0,1]         
 * @usage:
 */
function lock_image($request, $response, $args)
{
    global $app;
    global $db;

    $allowed_params = [
        'lot_id' => ['type' => 'int'],
        'image_id' => ['type' => 'int'],
        'lock' => [0, 1],
    ];

    $error = _check_params($allowed_params, $args);

    if(sizeof($error)>0){
        json_response($response, 200, $error);
    }

    if($args['lock'] == 1){
        $args['lock'] = time();
    }else{
        $args['lock'] = 0;
    }

    $sql = "UPDATE `training_images` SET `locked_time` = {$args['lock']} WHERE `lot_id` = {$args['lot_id']} AND `image_id` = {$args['image_id']}";
    $result = $db->query($sql);
    $data = ['args' => $args, 'error' => $error,'sql'=>$sql];

    return json_response($response, 200, $data);
}

/**
 * Gets next available image for classification or specific image if id is given
 * @getParams:
 *      daylight=[0,1]      default=0
 *      image_id=[N]
 *      order=[ASC,DESC]    default=ASC
 *      lock=[0,1]          default=0
 * @usage:
 *  get: http://cs.mwsu.edu/~griffin/p-lot/bolin_parking_lot/lot_image?daylight=1
 *  returns:
 *      all images taken between sunup and sundown
 *
 *  get: http://cs.mwsu.edu/~griffin/p-lot/bolin_parking_lot/lot_image?image_id=343
 *  returns:
 *      The image with id 343
 *
 *  get: http://cs.mwsu.edu/~griffin/p-lot/bolin_parking_lot/lot_image?image_id=343
 *  returns:
 *      The image with id 343
 *
 *  get: http://cs.mwsu.edu/~griffin/p-lot/bolin_parking_lot/lot_image?lock=1
 *  returns:
 *      Will lock whatever image it returns
 *
 *  get: http://cs.mwsu.edu/~griffin/p-lot/bolin_parking_lot/lot_image?lock=1&order=DESC
 *  returns:
 *      Will return latest previous un-classified image and lock it.
 */
function lot_image($request, $response, $args)
{
    global $app;
    global $db;
    $pdo = $app->getContainer()->get('pdo');
    $base_url = 'http://cs.mwsu.edu/~griffin/';

    $params = $request->getParams();
    $image_id = null;
    $order = null;
    $lock = false;
    $daylight = null;
    $date = null;

    $params = _build_params_array($request);

    if (array_key_exists('image_id', $params)) {
        $image_id = $params['image_id'];
    }

    if (array_key_exists('order', $params)) {
        $order = $params['order'];
    }

    if (array_key_exists('lock', $params)) {
        $lock = $params['lock'];
    }

    if (array_key_exists('daylight', $params)) {
        $daylight = $params['daylight'];
    }

    if (array_key_exists('date', $params)) {
        $date = $params['date'];
    }

    if (array_key_exists('prev', $params)) {
        $prev = $params['prev'];
    }

    //debug (print_r($pdo,true), date('Y-m-d H:i:s').": lot_image ", "./logs/output.log");
    $statement = $pdo->select();
    $statement->from('training_images');

    if ($image_id != null) {
        $statement->where('lot_id', '=', '1');
        $statement->where('image_id', '=', $image_id);
    } else {
        $statement->where('classified', '=', '0');
        $statement->where('locked_time', '=', '0');
    }
    if ($daylight != null) {
        $statement->where('daylight', '=', $daylight);
    }
    if ($date != null) {
        if($prev == 1){
            $statement->where('date_created', '<', $date);
        }
        else{
            $statement->where('date_created', '>', $date);
        }
    }
    if ($order == null) {
        $statement->orderBy('date_created', 'ASC');
    } else {
        $statement->orderBy('date_created', $order);
    }

    $statement->limit(1);

    $stmt = $statement->execute();
    $data['image_data'] = $stmt->fetch();

    //build link for front end
    $path = explode('/', $data['image_data']['path']);

    //debug(print_r($sql,true), date('Y-m-d H:i:s').": Path ", "./logs/output.log");

    if($data['image_data']['path'] == ""){
        return json_response($response, 200, "error");
    }
    else{
        for ($i = 0; $i < 4; $i++) {
            array_shift($path);
        }
        $data['image_data']['img_url'] = $base_url . implode('/', $path);

        //build thumblink for front end
        $path = explode('/', $data['image_data']['thumb_path']);
        for ($i = 0; $i < 4; $i++) {
            array_shift($path);
        }
        $data['image_data']['thumb_url'] = $base_url . implode('/', $path);

        $lid = $data['image_data']['lot_id'];
        $iid = $data['image_data']['image_id'];
        $data['locked'] = _lock_image($lid, $iid);
        $data['image_data']['locked_time'] = $data['locked'];

        return json_response($response, 200, $data);
    }
}




/**
 * Gets number of images
 * @getParams:
 *      classified=[0,1]      default=0
 *      user=[User Email]
 * @usage:
 *  get: http://cs.mwsu.edu/~griffin/p-lot/bolin_parking_lot/image_number?user=a@a.com
 *  returns:
 *      number of all images classified by a@a.com
 *
 *  get: http://cs.mwsu.edu/~griffin/p-lot/bolin_parking_lot/image_number?classified=1
 *  returns:
 *      number of all classified images
 *
 *  get: http://cs.mwsu.edu/~griffin/p-lot/bolin_parking_lot/image_number
 *  returns:
 *      number of all images
 */

function image_number($request, $response, $args)
{
    global $app;
    global $db;
    $pdo = $app->getContainer()->get('pdo');
    $base_url = 'http://cs.mwsu.edu/~griffin/';

    $params = $request->getParams();
    $user = null;
    $classified = null;


    $params = _build_params_array($request);

    if (array_key_exists('user', $params)) {
        $user = $params['user'];
    }
    if (array_key_exists('classified', $params)) {
        $classified = $params['classified'];
    }

    //debug (print_r($pdo,true), date('Y-m-d H:i:s').": lot_image ", "./logs/output.log");
    $statement = $pdo->select();
    $statement->from('training_images');

    $statement->where('lot_id', '=', '1');

    if ($user != null) {
        $statement->where('edited_by', '=', $user);
    }
    if ($classified != null) {
        $statement->where('classified', '=', $classified);
    }
    

    $stmt = $statement->execute();
    $data = $stmt->fetchall();
    $count = count($data);
    return json_response($response, 200, $count);

    //debug(print_r($sql,true), date('Y-m-d H:i:s').": Path ", "./logs/output.log");
}

/**
 * Gets an overlay for specified image
 * @Params:
 *     $request (object): request type
 *     $response (object): response type
 *     $args (object): get args
 */
function lot_overlay($request, $response, $args)
{
    global $app;
    global $db;

    $get = $request->getQueryParams();
    $post = $request->getParsedBody();

    //print_r($params);

    $lot_id = $args['lot_id'];
    $image_id = $args['image_id'];
    $lot_data = [];


    $sql = "SELECT  lot_data FROM `training_images` WHERE `lot_id` = {$lot_id} AND `image_id` = {$image_id}";
    $result = $db->query($sql);
    if($result)
        $row = $result->fetch_assoc();

    // $update = $pdo->update(array(, , ))
    //     ->table('training_images')
    //     ->where('lot_id', '=', $lot_id)
    //     ->where('image_id', '=', $image_id);

    $data = [];
    //$data['unlocked'] = _lock_image($lot_id, $image_id);
    $data['sql'] = $sql;
    $data['success'] = ($result !== false);
    $data['data'] = $row;


    return json_response($response, 200, $data);
}



/**
 * Gets next available image for classification
 * @Params:
 *     $request (object): request type
 *     $response (object): response type
 *     $args (object): get args
 */
function save_lot_image($request, $response, $args)
{
    global $app;
    global $db;
    //$pdo = $app->getContainer()->get('pdo');
    //debug (print_r($pdo,true), date('Y-m-d H:i:s').": lot_image ", "./logs/output.log");

    $get = $request->getQueryParams();
    $post = $request->getParsedBody();

    //print_r($params);
    
    $lot_id = $args['lot_id'];
    $image_id = $args['image_id'];
    $lot_data = json_encode($post['data']);
    $userEmail = $post['userEmail'];
    
    $dls = time();

    $sql = "UPDATE `training_images` SET `locked_time` = '', `date_last_saved` = '{$dls}', `classified` = 1, `lot_data` = '{$lot_data}', `edited_by` = '{$userEmail}'
    WHERE `lot_id` = {$lot_id} AND `image_id` = {$image_id}";

    //debug (print_r($sql,true), date('Y-m-d H:i:s').": lot_image ", "./logs/output.log");

    $result = $db->query($sql);

    
    // $update = $pdo->update(array(, , ))
    //     ->table('training_images')
    //     ->where('lot_id', '=', $lot_id)
    //     ->where('image_id', '=', $image_id);

    $data = [];
    //$data['unlocked'] = _lock_image($lot_id, $image_id);
    $data['sql'] = $sql;
    $data['success'] = ($result !== false);
    $data['args'] = $args;
    $data['post'] = $post;
    $data['get'] = $get;

    return json_response($response, 200, $data);
}

function _lock_image($lot_id, $image_id)
{
    global $app;
    $pdo = $app->getContainer()->get('pdo');

    $statement = $pdo->select()
        ->from('training_images')
        ->where('lot_id', '=', $lot_id)
        ->where('image_id', '=', $image_id);

    $stmt = $statement->execute();
    $image_data = $stmt->fetch();

    $locked = (int) $image_data['locked_time'];

    if ($locked > 0) {
        $locked_time = 0;
    } else {
        $locked_time = time();
    }

    $update = $pdo->update(array('locked_time' => $locked_time))
        ->table('training_images')
        ->where('lot_id', '=', $lot_id)
        ->where('image_id', '=', $image_id);
    if ($update->execute()) {
        return $locked_time;
    } else {
        return false;
    }

}

/**
 * @Params:
 *     $request (object): request type
 *     $response (object): response type
 *     $args (object): get args
 */
function camera($request, $response, $args)
{
    debug(print_r($request->getParsedBody(), true), date('Y-m-d H:i:s') . ": get_image ", "./logs/output.log");

    $data['type'] = 'Get';
    $data['qparams'] = $request->getQueryParams();
    $data['params'] = $request->getParams();

    $username = 'admin';
    $password = 'admin';
    $url = "http://10.0.61.76/live/0/jpeg.jpg";

    $context = stream_context_create(array(
        'http' => array(
            'header' => "Authorization: Basic " . base64_encode("$username:$password"),
        ),
    ));

    $image = file_get_contents($url, false, $context);

    $response->write($image);
    return $response->withHeader('Content-Type', FILEINFO_MIME_TYPE);
}

/**
 * poll_camera: snaps image and saves to path
 * @Params:
 *     $request (object): request type
 *     $response (object): response type
 *     $args (object): get args
 */
function trigger_camera($request, $response, $args)
{
    global $app;
    $pdo = $app->getContainer()->get('pdo');
    $data = $request->getParams();
    $basepath = $data['basepath'];

    $basepath = rtrim($basepath, "/");
    $basepath = $basepath . "/";

    $date = date("d-m-y", time());
    debug(print_r($basepath . $date, true), date('Y-m-d H:i:s') . ": base_path app", "./logs/output.log");
    if (!is_dir($basepath . $date)) {
        if (!mkdir($basepath . $date, 0777)) {
            die('Failed to create folders...');
        }
        chmod($basepath . $date, 0777);
    }
    if (is_dir($basepath . $date)) {
        $results = grab_snapshot($basepath . $date, true);
        debug(print_r($results, true), date('Y-m-d H:i:s') . ": trigger_camera app", "./logs/output.log");
    }

    $id = 0;

    $selectStatement = $pdo->select()->from('training_images');
    $selectID = $selectStatement->execute(false);
    $id = $selectStatement->count() + 1;

    debug(print_r($id, true), date('Y-m-d H:i:s') . ": id ", "./logs/output.log");

    // $insertStatement = $pdo->insert(array('lot_id', 'image_id', 'timestamp','path','json','classified'))
    //     ->into('training_images')
    //     ->values(array(1, 'your_username', 'your_password'));

    // $insertId = $insertStatement->execute(false);

    return json_response($response, 200, $results);
}

/**
 * @Params:
 *     $request (object): request type
 *     $response (object): response type
 *     $args (object): get args
 */
function example_handler($request, $response, $args)
{
    debug(print_r($request->getParsedBody(), true), date('Y-m-d H:i:s') . ": request ", "./logs/output.log");
    if ($request->isGet()) {
        $data['type'] = 'Get';
        $data['qparams'] = $request->getQueryParams();
        $data['params'] = $request->getParams();
    } else if ($request->isPost()) {
        $data['type'] = 'Post';
        $data['qparams'] = $request->getQueryParams();
        $data['params'] = $request->getParsedBody();
    }

    return json_response($response, 200, $data);
}

function json_response(&$response, $status, $data)
{
    return $response->withStatus($status)
        ->withHeader('Content-Type', 'application/json')
        ->write(json_encode($data));
}

/**
 * Upload image to waldo site
 *
 * @param
 *      $request (Request) posted values n such
 *      $response (Response) object
 *      $args (array) get arguments
 * @return
 */
function uploadImage($request, $response, $args)
{

    $files = $request->getUploadedFiles();

    debug(print_r($files, true), date('Y-m-d H:i:s') . ": Files ", "./logs/output.log");

    $uploaded_names = [];
    foreach ($files['files'] as $newfile) {
        debug($newfile, date('Y-m-d H:i:s') . ": newfile ", "./logs/output.log");
        if ($newfile->getError() === UPLOAD_ERR_OK) {
            debug($newfile, date('Y-m-d H:i:s') . ": name ", "./logs/output.log");
            $uploaded_names[] = moveUploadedFile('./file_uploads', $newfile);
        }
    }
    return json_response($response, 200, ['success' => true, 'filenames' => $uploaded_names]);
}

/**
 * Moves the uploaded file to the upload directory and assigns it a unique name
 * to avoid overwriting an existing uploaded file.
 *
 * @param string $directory directory to which the file is moved
 * @param UploadedFile $uploaded file uploaded file to move
 * @return string filename of moved file
 */
function moveUploadedFile(string $directory, Slim\Http\UploadedFile $uploadedFile)
{
    $extension = pathinfo($uploadedFile->getClientFilename(), PATHINFO_EXTENSION);
    $basename = bin2hex(random_bytes(8)); // see http://php.net/manual/en/function.random-bytes.php
    $filename = sprintf('%s.%0.8s', $basename, $extension);

    $uploadedFile->moveTo($directory . DIRECTORY_SEPARATOR . $filename);

    return $filename;
}

function _build_params_array($request)
{
    $params = [];
    foreach ($request->getParams() as $key => $value) {
        $params[$key] = $value;
    }
    foreach ($request->getQueryParams() as $key => $value) {
        $params[$key] = $value;
    }
    return $params;
}
/**
 * _check_params
 *
 * @param [array] $allowed
 * @param [array] $params
 * @return void
 */
function _check_params($allowed, $args)
{

    // $allowed = [
    //     'lot_id' => ['type'=>'int'],
    //     'image_id' => ['type'=>'int'],
    //     'lock' => [0,1]
    // ];

    // $args = {
    //     "lot_id": "1",
    //     "image_id": "1",
    //     "lock": "1"
    // }

    foreach ($args as $k => $v) {
        //debug(print_r([$k, $v], true), date('Y-m-d H:i:s') . ": key - value ", "./logs/output.log");
        if (!array_key_exists($k, $allowed)) {
            return ["error" => 1, "description" => "Unknown key name:'{$k}'."];
        } else if (array_key_exists('type', $allowed[$k])) {
            $type = $allowed[$k]['type'];
            //debug(print_r([$type], true), date('Y-m-d H:i:s') . ": $type  ", "./logs/output.log");
            if ($type == 'int' && !is_numeric($args[$k])) {
                return ["error" => 1, "description" => "Key:'{$k}' is not numeric."];
            }
            //more later maybe
        } else {
            //in_array messed with me
            // $match = 0;
            // foreach ($allowed[$k] as $tval) {
            //     if ($args[$k] == $tval) {
            //         $match = 1;
            //     }
            // }
            // if ($match) {
            //     return ["error" => 1, "description" => "Unknown value:'{$args[$k]}' not allowed as a value for {$k}."];
            // }
        }
    }
    return [];

};

function _error_handler($response, $error)
{
    return $response->withStatus(200)
        ->withHeader('Content-Type', 'application/json')
        ->write(json_encode($error));
}
/****************************************************************************************************
 * MODELS
 ****************************************************************************************************/
