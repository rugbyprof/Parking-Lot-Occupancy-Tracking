<?php
$settings = include('settings.php');
//$debug = include('debug.php');
$settings = $settings['mysql'];
$host = $settings['host'];
$db   = $settings['dbname'];
$user = $settings['user'];
$pass = $settings['pass'];
$charset = 'utf8mb4';

$dsn = "mysql:host=$host;dbname=$db;charset=$charset";
$opt = [
    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES   => false,
];

$pdo = new PDO($dsn, $user, $pass, $opt);

function grab_snapshot($path=false,$make_thumb=false){
    global $pdo;
    $path = rtrim($path,'/');
    $path = $path.'/';
    $daylight = 0;

    $username = 'admin';
    $password = 'admin';
    $url = "http://10.0.61.76/live/0/jpeg.jpg";
     
    $context = stream_context_create(array(
        'http' => array(
            'header'  => "Authorization: Basic " . base64_encode("$username:$password")
        )
    ));

    $image = file_get_contents($url, false, $context);

    if($image){
        if(!$path){
            return $image;
        }
        $t = time();
        $filename  = "{$path}{$t}.jpg";
        $weathername = "{$path}{$t}.json";
        file_put_contents($filename,$image);
        $weather_json = json_decode(file_get_contents("http://api.openweathermap.org/data/2.5/weather?zip=76308&appid=7121f0abc97aacff5b6044b0970718e0"),true);
        $words = [];
        if(is_array($weather_json)){
            foreach($weather_json['weather'] as $w){
                $words[] = $w['main'];
            }
            $sunrise = $weather_json['sys']['sunrise'];
            $sunset = $weather_json['sys']['sunset'];
            $dt = $weather_json['dt'];
            if($dt>$sunrise && $dt<$sunset){
                $daylight = 1;
            }
        }
        
        $wkeys = implode(',',$words);



        //debug (print_r($wkeys,true), date('Y-m-d H:i:s').": weather keys ", "./logs/output.log");

        file_put_contents($weathername,json_encode($weather_json)) ;
        if($make_thumb){
            $thumb_name  = "{$path}{$t}_thumb.jpg";
            make_thumb($filename, $thumb_name , 300);
            $data = [1,0,$t,"","{$filename}","{$thumb_name}","",0,$wkeys,json_encode($weather_json),0,"",$daylight];
            insert_image_data($data);
            return ['filename'=>$filename,'thumbname'=>$thumb_name];
        }else{
            return $filename;
        }
    }else{
        return false;
    }
}

function insert_image_data($data){
    global $pdo;
    $sql = "SELECT MAX(image_id) + 1 FROM training_images;";
    $statement = $pdo->prepare($sql);
    $statement->execute(); 
    $data[1] = $statement->fetchColumn();
    $sql = "INSERT INTO `training_images` (`lot_id`, `image_id`, `date_created`, `date_last_saved`,`path`, `thumb_path`, `lot_data`, `classified`, `weather_keywords`, `weather_json`,`locked_time`,`edited_by`,`daylight`) 
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)";
    //debug (print_r($data,true), date('Y-m-d H:i:s').": sql insert image ", "./logs/output.log");
    $pdo->prepare($sql)->execute($data);
}

function make_thumb($src, $dest, $desired_width) {
    
    /* read the source image */
    $source_image = imagecreatefromjpeg($src);
    $width = imagesx($source_image);
    $height = imagesy($source_image);

    /* find the "desired height" of this thumbnail, relative to the desired width  */
    $desired_height = floor($height * ($desired_width / $width));

    /* create a new, "virtual" image */
    $virtual_image = imagecreatetruecolor($desired_width, $desired_height);

    /* copy source image at a resized size */
    imagecopyresampled($virtual_image, $source_image, 0, 0, 0, 0, $desired_width, $desired_height, $width, $height);

    /* create the physical thumbnail image to its destination */
    imagejpeg($virtual_image, $dest);
}


function grab_snapshot2($path='.',$save_image=false,$make_thumb=false){
    $path = rtrim($path,'/');
    $path = $path.'/';

    $curl = curl_init();

    curl_setopt_array($curl, array(
    CURLOPT_URL => "http://10.0.61.76/live/0/jpeg.jpg",
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_ENCODING => "",
    CURLOPT_MAXREDIRS => 10,
    CURLOPT_TIMEOUT => 30,
    CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
    CURLOPT_CUSTOMREQUEST => "GET",
    CURLOPT_POSTFIELDS => "",
    CURLOPT_HTTPHEADER => array(
        "authorization: Basic YWRtaW46YWRtaW4=",
        "cache-control: no-cache",
        "content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        "postman-token: c1d37a0a-c220-f26f-ec09-0649ed6f4de2"
    ),
    ));

    $response = curl_exec($curl);
    $err = curl_error($curl);

    curl_close($curl);

    if ($err) {
        echo "cURL Error #:" . $err;
    } else {
        $t = time();
        $filename  = "{$path}{$t}.jpg";

        if(!$save_image){
            return $response;
        }
        file_put_contents($filename,$response);
        if($make_thumb){
            $thumb_name  = "{$path}{$t}_thumb.jpg";
            make_thumb($filename, $thumb_name , 300);
            return ['filename'=>$filename,'thumbname'=>$thumb_name];
        }else{
            return $filename;
        }
    }
}
?>
