SPIRLe > IDE
======

Code and required additional files for various components of the front-end IDE (Integrated Development Environment) interface.

Prerequisites
-------------
Python 2.7, PyQt 4

Instructions on running IDE:

IDE in Executable file:
1.  Double click on the executable file

IDE in Python Code:
1.	Install Python and PyQt4, if it is not already installed. For Python, choose the version 2.7 not 3.x
2.	Go to the directory where the IDE is, and execute “python frame.py”

How to use IDE:
1.	There is a tool window on the left. You can see many blocks available to use. Drag one of the blocks, and drop it to the white screen in the tab that says New.
2.	You can see that the block is dropped onto the screen. You can chain the blocks from top to bottom, and that is your new programme. For the actual python code generated from blocks, you can see it in the Code tab on the bottom.
3.	Some blocks can be edited. After you dropped a block onto the screen, you can double click on the block to edit it. For example, if you use move forward block, you can edit the speed and distance. When you finish editing, press OK button. There is an edit block which is for advanced users, and in the edit block, you can also save the edited block to a file by pressing Save button. Saved edited blocks can be loaded by pressing Edit -> Load Edit Block or pressing Ctrl+L.
4.	Blocks can be deleted by dragging the block to the delete block. Alternatively, you can also delete the block by selecting the block and pressing delete or backspace key.
5.	Blocks can be copied and paste as well. You can drag and drop the block you want to copy into the Copy block. When you want to paste the block, just simply drag and drop the copy block.
6.	You can use conditional blocks as well. Conditional blocks are the red blocks. You can edit the condition by double clicking on the conditional block. When you drag and drop a block on the right of the conditional block, the conditional block splits. You can put as many blocks as you want into the conditional block, and they extends to the right.
7.	When you finish building blocks, you can save it to a file. Press File -> Save or press Ctrl+S. Also, you can use File -> Save as or Shift+Ctrl+S. You can also open file by pressing File -> Open File or Ctrl+O. If you just want to open a new tab, press File -> New File or Ctrl+N.
8.	When you want to run the code, there are two options. If you press File -> Run or Ctrl+R, then the code will run on the actual robot.(However there is some issue with this now) If you press File -> Run in the simulator or Shift+Ctrl+R, then the code will run in the simulator. In order to run in the simulator, you need to run the simulator. In order to run Mark Handley’s simulator, go to the directory and then execute python RoboSim

