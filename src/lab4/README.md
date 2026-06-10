# Lab 04b - Robot Architecture - ROS

Dieses Package implementiert eine autonome Steuerung eines Turtlebot3 (waffle_pi) Roboters unter Verwendung von ROS Noetic. Es wurden mehrere ROS-Nodes entwickelt, die miteinander kommunizieren und verschiedene Aufgaben übernehmen.

## Voraussetzungen

- Ubuntu 20.04
- ROS Noetic
- Turtlebot3 Packages (`turtlebot3`, `turtlebot3_msgs`, `turtlebot3_simulations`)
- Python 3
- cv_bridge, OpenCV (`ros-noetic-cv-bridge`, `ros-noetic-vision-opencv`)

## Package Struktur
lab4/
├── launch/
│   ├── wall_follower.launch         # Startet alle Nodes für Wall Follower
│   ├── move_between_objects.launch  # Startet alle Nodes für Move Between Objects
│   └── two_objects_world.launch     # Startet Gazebo mit eigenem Umgebungsmodell
├── msg/
│   └── RobotStatus.msg              # Custom Message Definition
├── scripts/
│   ├── camera_node.py               # Kameraverarbeitung mit OpenCV
│   ├── status_publisher.py          # Publiziert RobotStatus Nachrichten
│   ├── logger_node.py               # Loggt RobotStatus in JSON Datei
│   ├── wall_follower.py             # Wall Follower Node
│   └── move_between_objects.py      # Move Between Objects Node
├── srv/
│   └── SetLogging.srv               # Service Definition für Logging
└── worlds/
└── two_objects.world            # Eigenes Gazebo Umgebungsmodell

## Nodes

### camera_node.py
Abonniert das Kamerabild des Turtlebot3 (`/camera/rgb/image_raw`) und verarbeitet es mit OpenCV. Es wird eine Kantendetektion (Canny Edge Detection) durchgeführt und das Ergebnis in einem OpenCV-Fenster angezeigt. Verwendet die ROS-OpenCV-Bridge (`cv_bridge`) zur Konvertierung zwischen ROS Image Messages und OpenCV Bildern.

### status_publisher.py
Abonniert `/cmd_vel` (aktuelle Geschwindigkeitsbefehle) und `/scan` (LiDAR Daten) und publiziert daraus eine eigene `RobotStatus` Nachricht auf dem Topic `/robot_status`. Die Nachricht enthält den aktuellen Geschwindigkeitsbefehl sowie die Abstände vorne, links und rechts gemessen vom LiDAR.

### logger_node.py
Abonniert `/robot_status` und schreibt die empfangenen Daten mit Timestamp in eine JSON-Datei (`~/robot_log.json`). Das Logging kann über den Service `/set_logging` ein- und ausgeschaltet werden. Bei deaktiviertem Logging werden keine neuen Einträge geschrieben.

### wall_follower.py
Implementiert einen regelbasierten Wall Follower. Der Roboter fährt vorwärts bis er auf eine Wand trifft, dreht dann und folgt der Wand entlang. Verwendet ausschließlich LiDAR-Daten (`/scan`) zur Steuerung und publiziert Geschwindigkeitsbefehle auf `/cmd_vel`.

### move_between_objects.py
Erkennt zwei Objekte mittels LiDAR (vorne und hinten) und fährt kontinuierlich zwischen diesen hin und her. Der Roboter wird zu Beginn zwischen die zwei Objekte platziert. Wechselt den Zustand zwischen `forward` und `backward` basierend auf den gemessenen Abständen.

## Custom Message: RobotStatus.msg
geometry_msgs/Twist cmd_vel    # Aktueller Geschwindigkeitsbefehl
float32 front_distance         # Abstand zur Wand/Objekt vorne (in Metern)
float32 left_distance          # Abstand zur Wand/Objekt links (in Metern)
float32 right_distance         # Abstand zur Wand/Objekt rechts (in Metern)

## Service: SetLogging.srv

Ermöglicht das Ein- und Ausschalten des Loggings zur Laufzeit.
bool enable      # true = Logging aktivieren, false = deaktivieren
bool success     # true wenn erfolgreich

Aufrufen über:
```bash
rosservice call /set_logging "enable: false"   # Logging ausschalten
rosservice call /set_logging "enable: true"    # Logging einschalten
```

## Ausführen

### Wall Follower

Terminal 1 – Simulationsumgebung starten:
```bash
roslaunch turtlebot3_gazebo turtlebot3_world.launch
```

Terminal 2 – Nodes starten:
```bash
roslaunch lab4 wall_follower.launch
```

### Move Between Objects

Terminal 1 – Eigene Umgebung mit zwei Objekten starten:
```bash
roslaunch lab4 two_objects_world.launch
```

Terminal 2 – Nodes starten:
```bash
roslaunch lab4 move_between_objects.launch
```
