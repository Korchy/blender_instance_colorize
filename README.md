# Instances Colorizer
Add-on functionality
-
Blender 3D add-on for easily coloring instances (objects using the same data block) in the 3D viewport.

The add-on automatically colorizes objects instances. To colorize instances in an existing scene, click the “Colorize Instances” button in the add-on panel.

Instances colors are visible in the 3D viewport area in Shading Mode – Object.

<img src="https://b3d.interplanety.org/wp-content/upload_content/2021/11/preview_01_1200x600-560x280.jpg"><p>

The add-on colorizes instances in two modes: Multi-Color – each group of instances is assigned a different color and Single-Color – all instances in the scene are colored with the same color.

In Multi-Color mode, the color of any instance group can be changed in the add-on panel.

If there are already instances of the current object in the scene, when a new instance is created, it is assigned the same color that is already assigned to all other instances of this object.

If there were no other instances of the current object in the scene before, the created instances are assigned a random color.

When an object that has no instances is added to the scene, it is assigned a base color.

The object Viewport Display – Color property is used to display instances colors.

Current add-on version
-
1.1.0.

Blender versions
-
2.93, 3.0, 3.1

Location and call
-
The “3D Viewport” window – N panel – “IC” tab.

Installation
-
- Download the *.zip archive with the add-on distributive.
- The “Preferences” window — Add-ons — Install… — specify the downloaded archive.

Version history
-
1.1.0.
- Added colorization for curve and text instances

1.0.0.
- This release.
