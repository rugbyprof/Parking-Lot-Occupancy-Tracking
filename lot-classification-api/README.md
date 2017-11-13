GET
  - get_lot_image: 
      - Will get a specified image from collection if ID is specified.
      - No specified ID will return next unclassified image in set.
      - retuns last saved date and last saved user
      - When image is checked out, it will display a:
        - "locked = true"
        - along with a  "time locked"
        - time locked expires when next user needs it if not saved after 5 minutues.
        
  - get_previous_unclassified_image
    -return id of previous unlocked, unclassified image
  
  - get_next_unclassified_image
    - -return id of next unlocked, unclassified image
POST




PUT
  - save_lot_image:
    - Will add [json data] for the specified image via ID.
    - return success or failure notice
    - Image checked out status goes to:
        - "locked = false"
        - "classified" = "true"
        - "date_classified" = "[<datetime>]"
        - "user_saved" = "[<username or userid>]"
        - "verified" = "true"
  - if lot classification json differs from existing json data:
        - append [json data]
        - "mismatch" = "true"
  - "corrupted" : true
  - "currupted_description": string
  

DELETE

