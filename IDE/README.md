SPIRLe > IDE
======

IDE!

Platforms
---------
Should work fine on both Windows and Linux for ordinary IDE use and simulation. Linux only for use with actual robots at the moment.

Prerequisites
-------------
Python 2.7.x branch
PyQt 4

Additional Prerequisites (for running code on Mark Handley robots)
------------------------
ssh
sshpass

Running the IDE
---------------
We have distributed some packaged binaries which should automatically run the IDE with no prereqs (availability and success may vary!)

Alternatively, running "python frame.py" in the IDE code directory should work on any platform as long as you have the prereqs!

Partial instructions for use
----------------------------
1.	There is a tool window on the left. You can see many blocks available to use. Drag one of the blocks, and drop it to the white screen in the tab that says New.
2.	You can see that the block is dropped onto the screen. You can chain the blocks from top to bottom, and that is your new programme. For the actual python code generated from blocks, you can see it in the Code tab on the bottom.
3.	Some blocks can be edited. After you dropped a block onto the screen, you can double click on the block to edit it. For example, if you use move forward block, you can edit the speed and distance. When you finish editing, press OK button. There is an edit block which is for advanced users, and in the edit block, you can also save the edited block to a file by pressing Save button. Saved edited blocks can be loaded by pressing Edit -> Load Edit Block or pressing Ctrl+L.
4.	Blocks can be deleted by dragging the block to the delete block. Alternatively, you can also delete the block by selecting the block and pressing delete or backspace key.
5.	Blocks can be copied and paste as well. You can drag and drop the block you want to copy into the Copy block. When you want to paste the block, just simply drag and drop the copy block.
6.	You can use conditional blocks as well. Conditional blocks are the red blocks. You can edit the condition by double clicking on the conditional block. When you drag and drop a block on the right of the conditional block, the conditional block splits. You can put as many blocks as you want into the conditional block, and they extends to the right.
7.	When you finish building blocks, you can save it to a file. Press File -> Save or press Ctrl+S. Also, you can use File -> Save as or Shift+Ctrl+S. You can also open file by pressing File -> Open File or Ctrl+O. If you just want to open a new tab, press File -> New File or Ctrl+N.
8.	When you want to run the code, there are two options. If you press File -> Run or Ctrl+R, then the code will run on the actual robot.(However there is some issue with this now) If you press File -> Run in the simulator or Shift+Ctrl+R, then the code will run in the simulator. In order to run in the simulator, you need to run the simulator. In order to run Mark Handley’s simulator, go to the directory and then execute python RoboSim