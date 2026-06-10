
# Lab 04b - Robot Architecture - ROS

Dieses Package implementiert eine autonome Steuerung eines Turtlebot3 (waffle_pi) Roboters unter Verwendung von ROS Noetic.

## Voraussetzungen

- Ubuntu 20.04
- ROS Noetic
- Turtlebot3 Packages
- Python 3
- cv_bridge, OpenCV

## Package Struktur

    lab4/
    ├── launch/
    │   ├── wall_follower.launch
    │   ├── move_between_objects.launch
    │   └── two_objects_world.launch
    ├── msg/
    │   └── RobotStatus.msg
    ├── scripts/
    │   ├── camera_node.py
    │   ├── status_publisher.py
    │   ├── logger_node.py
    │   ├── wall_follower.py
    │   └── move_between_objects.py
    ├── srv/
    │   └── SetLogging.srv
    └── worlds/
        └── two_objects.world

## Nodes

### camera_node.py
Abonniert das Kamerabild des Turtlebot3 und verarbeitet es mit OpenCV (Canny Edge Detection). Zeigt das Ergebnis in einem OpenCV-Fenster an.

### status_publisher.py
Abonniert `/cmd_vel` und `/scan` und publiziert eine `RobotStatus` Nachricht auf `/robot_status` mit aktuellem Geschwindigkeitsbefehl und LiDAR-Abständen.

### logger_node.py
Abonniert `/robot_status` und schreibt die Daten mit Timestamp in eine JSON-Datei (`~/robot_log.json`). Kann per Service ein/ausgeschaltet werden.

### wall_follower.py
Regelbasierter Wall Follower. Fährt vorwärts bis zur Wand, dreht dann und folgt der Wand entlang.

### move_between_objects.py
Fährt kontinuierlich zwischen zwei Objekten hin und her, basierend auf LiDAR-Messungen vorne und hinten.

## Custom Message: RobotStatus.msg

    geometry_msgs/Twist cmd_vel
    float32 front_distance
    float32 left_distance
    float32 right_distance

## Service: SetLogging.srv

    bool enable
    ---
    bool success

Ein/Ausschalten per Terminal:

    rosservice call /set_logging "enable: false"
    rosservice call /set_logging "enable: true"

## Ausführen

### Wall Follower

Terminal 1:

    roslaunch turtlebot3_gazebo turtlebot3_world.launch

Terminal 2:

    roslaunch lab4 wall_follower.launch

### Move Between Objects

Terminal 1:

    roslaunch lab4 two_objects_world.launch

Terminal 2:

    roslaunch lab4 move_between_objects.launch
