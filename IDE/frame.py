#coding:utf-8

#by Teruki Tauchi
#website referred http://zetcode.com/tutorials/pyqt4/

import sys
import os
import subprocess
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import StringIO
import window
import socket
from robosim import *
sys.path.insert(0,"/home/ubuntu/python/program/ide/robo-sim")
import src.simulator

# Many of this is not currently implemented yet
# I will change in the future

class IDEWindow(QtGui.QMainWindow):
	def __init__(self, parent=None):
        	super(IDEWindow, self).__init__(parent)
		self.initUI()

	def action(self, act):
		if act == 0:
			return self.newFile
		if act == 1:
			return self.openFile
		if act == 2:
			return self.saveFile
		if act == 3:
			return self.saveAs
		if act == 4:
			return self.runCode
		if act == 5:
			return self.runSim
		if act == 6:
			return self.close
		if act == 7:
			return self.loadBlock
		else:
			#not implemented yet
			return self.nothing

	def initUI(self):
		# Variable Declerations
		self.isSaved = True
		self.fileName = "New"
		self.outputScreen = ""
		self.openFiles = ["New"]
		self.openFileNames = [None]
		bottomTabOpen = ["Debug","Output","Sensor","Code"]
		# Set Window Title
		self.setWindowTitle("SPIRLe v1.0")
		# Set Icon
		self.setWindowIcon(QtGui.QIcon("images/icon.png"))

		# Menu Actions
		actionNameList = [
		"&New File", "&Open File", "&Save File", "&Save File As...", "&Run", "&Run in the simulator", "&Quit",
		"&Load Edit Block", "&Undo", "&Redo", "&Cut", "&Copy", "&Paste", "&Preference",
		"&ToolBox", "&Block Editor", "&Debug Screen", "&Output Screen", "&Sensor Screen", "&Code Screen", "&Folder Screen",
		"&Help"]
		shortCutList = [
		"Ctrl+N", "Ctrl+O", "Ctrl+S", "", "Ctrl+R", "Ctrl+Shift+R", "Ctrl+Q",
		"Ctrl+L", "Ctrl+Z", "Ctrl+Y", "Ctrl+X", "Ctrl+C", "Ctrl+V", "",
		"", "", "", "", "", "", "",
		"Ctrl+H"]
		actionList = []
		for i in range(len(actionNameList)):
			a = QtGui.QAction(actionNameList[i], self)
			a.setShortcut(shortCutList[i])
			a.triggered.connect(self.action(i))
			actionList.append(a)

		# Menu
        	self.file_menu = self.menuBar().addMenu("&File")
        	for i in range(7):
			self.file_menu.addAction(actionList[i])

        	self.edit_menu = self.menuBar().addMenu("&Edit")
        	for i in range(7,14):
			self.edit_menu.addAction(actionList[i])

		self.view_menu = self.menuBar().addMenu("View")
		for i in range(14,21):
			self.view_menu.addAction(actionList[i])

		self.help_menu = self.menuBar().addMenu("Help")
		self.help_menu.addAction(actionList[21])

		# Main Window
		self.main = QtGui.QWidget(self)

		hbox = QtGui.QHBoxLayout(self.main)

		self.toolbox = QtGui.QDockWidget("Tool Box",self.main)
		self.toolbox.setWidget(window.ToolWindow(self))

		self.screentab = QtGui.QTabWidget(self.main)
		self.screentab.setTabsClosable(True)
		self.screentab.setMovable(True)
		self.programmeList = []
		for i in range(len(self.openFiles)):
			pl = window.ProgrammeWindow(self)
			pw = self.screentab.addTab(pl,self.openFiles[i])
			self.programmeList.append(pl)
		self.screentab.currentChanged.connect(self.refreshCode)

		v = QtGui.QSplitter(QtCore.Qt.Vertical)
		self.copy = window.CopyDeleteWindow(self,"Copy")
		self.delete = window.CopyDeleteWindow(self,"Delete")
		v.addWidget(self.copy)
		v.addWidget(self.delete)
		v.setSizes([100,100])
		
		self.folder = QtGui.QDockWidget("Folder",self.main)
		self.folder.setWidget(window.FolderWindow(self))

		self.bottomtab = QtGui.QTabWidget(self.main)
		self.bottomtab.setTabsClosable(True)
		self.bottomtab.setMovable(True)
		self.bottomtabList = []
		for i in range(len(bottomTabOpen)):
			btl = window.TabWindow(self,bottomTabOpen[i])
			self.bottomtab.addTab(btl,bottomTabOpen[i])
			self.bottomtabList.append(btl)

		toprow = QtGui.QSplitter(QtCore.Qt.Horizontal)
		toprow.addWidget(self.toolbox)
		toprow.addWidget(self.screentab)
		toprow.addWidget(v)
		toprow.setSizes([300,460,200])

		bottomrow = QtGui.QSplitter(QtCore.Qt.Horizontal)
		bottomrow.addWidget(self.folder)
		bottomrow.addWidget(self.bottomtab)
		bottomrow.setSizes([300,660])

		splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
		splitter.addWidget(toprow)
		splitter.addWidget(bottomrow)
		splitter.setSizes([340,200])

		hbox.addWidget(splitter)
		self.main.setLayout(hbox)
		QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
		self.setCentralWidget(self.main)
		
	def closeEvent(self, event):
	# temporarily putting closeEvent as closedEvent so that window can close smoothly
		if(self.isSaved):
			reply = QtGui.QMessageBox.question(self, 'Message',"Are you sure to quit?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
		else:
			reply = QtGui.QMessageBox.question(self, 'Message',"Changes in the File not Saved!\nAre you sure to quit?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
		
		if reply == QtGui.QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()

	def nothing(self):
		return

	def newFile(self):
		self.openFiles.append("New")
		self.openFileNames.append(None)
		pl = window.ProgrammeWindow(self)
		self.screentab.addTab(pl,"New")
		self.programmeList.append(pl)
		return

	def openFile(self):
		fileName = QtGui.QFileDialog.getOpenFileName()
		if not fileName.isEmpty():
			f = file(fileName)
			self.bottomtabList[3].textEdit.setPlainText(f.read())

	def saveFile(self):
		index = self.screentab.currentIndex()
		fileName = self.openFileNames[index]
		if fileName == None:
			self.saveAs()
			return
		else:
			f = file(fileName, "w")
			content = self.bottomtabList[3].textEdit.toPlainText()
			f.write(content)

	def saveAs(self):
		index = self.screentab.currentIndex()
		fileName = QtGui.QFileDialog.getSaveFileName()
		if not fileName.isEmpty():
			f = file(fileName, "w")
			content = self.bottomtabList[3].textEdit.toPlainText()
			f.write(content)
			self.openFileNames[index] = str(fileName)
			self.openFiles[index] = os.path.basename(str(fileName))
			self.screentab.setTabText(index,self.openFiles[index])
			

	def runCode(self):
		self.saveFile()
		bashCommand = "sshpass -p \"localuser\" scp -o \"StrictHostKeyChecking no\" program.py robosim.py localuser@128.16.79.5:;sshpass -p \"localuser\" ssh -o \"StrictHostKeyChecking no\" localuser@128.16.79.5 python program.py"
		os.system(bashCommand)

	def runSim(self):
		buffer = StringIO.StringIO()
		sys.stdout = buffer
		exec str(self.bottomtabList[3].textEdit.toPlainText())
		sys.stdout = sys.__stdout__
		self.outputScreen = buffer.getvalue()
		self.bottomtabList[1].textEdit.setPlainText(self.outputScreen)

	def loadBlock(self):
		fileName = QtGui.QFileDialog.getOpenFileName()
		if not fileName.isEmpty():
			f = file(fileName)
			content = f.read()
			toollist = self.toolbox.widget().tableList
			row = toollist.rowCount()
			toollist.setRowCount(row+1)
			mainFunc = """def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('localhost', 55443))"""
			if content == None:
				QtGui.QMessageBox.information(self, 'Message',"Failed to load content of file. Isn't it empty?", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
				if reply == QtGui.QMessageBox.Ok:
					return
			if content.find(mainFunc) == -1 or content.find("s.close()\n") == -1:
				QtGui.QMessageBox.information(self, 'Message',"File is not in the correct format. Please load file that is created by this IDE.", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
				if reply == QtGui.QMessageBox.Ok:
					return
			edit = "#Edit Block" + content[content.find(mainFunc)+len(mainFunc):content.find("s.close()\n")] + "#End of Edit Block"

			editItem = QtGui.QTableWidgetItem()
			editItem.setIcon(QtGui.QIcon("images/edit.png"))
			editItem.setSizeHint(QtCore.QSize(100,100))
			editItem.setWhatsThis(edit)
			toollist.setItem(row,0,editItem)

			nameItem = QtGui.QTableWidgetItem()
			name = os.path.basename(str(fileName))
			nameItem.setText(name)
			nameItem.setFlags(QtCore.Qt.ItemIsEnabled)
			toollist.setItem(row,1,nameItem)

	def refreshCode(self):
		window.refreshCode(self)

def main():
	a = QtGui.QApplication(sys.argv)

	window = IDEWindow()
	window.resize(960,540)
	window.show()

	sys.exit(a.exec_())

if __name__ == "__main__":
	main()
