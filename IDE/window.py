#coding:utf-8

#by Teruki Tauchi

import sys
import os
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import syntax

testNames = ["flashLED()", "moveForward(s,30,300)", "turnLeft(s)", "turnRight(s)", "while True:", "#If-else block", "#Edit Block\n\t#End of Edit Block"]

class ProgrammeWindow(QtGui.QWidget):
	def __init__(self, parent, fileName):
        	super(ProgrammeWindow, self).__init__(None)
		self.initUI(parent)

	def initUI(self,parent):
		hbox = QtGui.QHBoxLayout()
		self.tableWidget = CustomisedTable(parent)
		self.tableWidget.resize(680,330)
		h = self.tableWidget.horizontalHeader()
		h.setDefaultSectionSize(130)
		h.setVisible(False)
		v = self.tableWidget.verticalHeader()
		v.setDefaultSectionSize(130)
		v.setVisible(False)
		self.tableWidget.setColumnCount(3)
		self.tableWidget.setRowCount(10)
		self.tableWidget.setShowGrid(False)
		self.tableWidget.setIconSize(QtCore.QSize(130,130))
		
		self.tableWidget.setAcceptDrops(True)
		self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
		self.tableWidget.setDragEnabled(True)
		hbox.addWidget(self.tableWidget)
		self.setLayout(hbox)

class FolderWindow(QtGui.QWidget):
	def __init__(self, parent=None):
        	super(FolderWindow, self).__init__(parent)

class TabWindow(QtGui.QWidget):
	def __init__(self, parent, windowType):
        	super(TabWindow, self).__init__(None)
		self.windowType = windowType
		self.parent = parent
		self.initUI()

	def initUI(self):
		self.textEdit = QtGui.QTextEdit(self)
		self.textEdit.setText(self.getText())
		if self.windowType == "Code":		
			test = syntax.PythonHighlighter(self.textEdit.document())
		#layout
		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(self.textEdit)
		self.setLayout(hbox)

	def getText(self):
		if self.windowType == "Code":
			value = self.parent.programmeList[0].tableWidget.returnCode()
			return value
		elif self.windowType == "Output":
			value = self.parent.outputScreen
			return value
		else:
			return ""

class ToolWindow(QtGui.QWidget):
	def __init__(self, parent):
        	super(ToolWindow, self).__init__(None)
		self.initUI()

	def initUI(self):
		#Variable Declaration
		blockIcons = ["flash.png", "forward.png", "turnleft.png", "turnright.png", "repeat.png", "ifelse.png", "edit.png"]
		blockNames = ["Flash LED", "Move Forward", "Turn Left", "Turn Right", "Repeat", "If-Else", "Edit"]
	
		for i in range(len(blockIcons)):
			blockIcons[i] = "images/" + blockIcons[i]

		#Table for list
		hbox = QtGui.QHBoxLayout()
		tableList = QtGui.QTableWidget(self)
		tableList.setIconSize(QtCore.QSize(100,100))
		tableList.resize(255,300)
		tableList.setDragEnabled(True)
		tableList.setColumnCount(2)
		tableList.setRowCount(len(blockIcons))
		h = tableList.horizontalHeader()
		h.setDefaultSectionSize(110)
		h.setVisible(False)
		v = tableList.verticalHeader()
		v.setDefaultSectionSize(110)
		v.setVisible(False)
		tableList.setShowGrid(False)

		for i in range(len(blockIcons)):
			iconItem = QtGui.QTableWidgetItem()
			icon = QtGui.QIcon(blockIcons[i]) 
			iconItem.setIcon(icon)
			iconItem.setSizeHint(QtCore.QSize(100,100))
			iconItem.setWhatsThis(testNames[i])
			tableList.setItem(i,0,iconItem)

			nameItem = QtGui.QTableWidgetItem()
			nameItem.setText(blockNames[i])
			nameItem.setFlags(QtCore.Qt.ItemIsEnabled)
			tableList.setItem(i,1,nameItem)

		tableList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
		hbox.addWidget(tableList)
		self.setLayout(hbox)

class CopyDeleteWindow(QtGui.QPushButton):
	def __init__(self, parent, mode):
        	super(CopyDeleteWindow, self).__init__(None)
		self.parent = parent
		self.mode = mode
		self.value = None
		self.initUI()

	def initUI(self):
		self.fileName =""
		if self.mode == "Copy":
			self.fileName = "images/copy.png"
		elif self.mode == "Delete":
			self.fileName = "images/delete.png"
		icon = QtGui.QIcon(self.fileName)
		self.setIcon(icon)
		self.setIconSize(QtCore.QSize(150,150))
		self.setAcceptDrops(True)
		self.tableWidget = QtGui.QTableWidget()

	def hitButton(self, event):
		return False

	def dragEnterEvent(self, event):
		event.accept()

	def dropEvent(self, event):
		if self.mode == "Copy":
			self.copyItems()
		elif self.mode == "Delete":
			self.deleteItems()
		else:
			return

	def copyItems(self):
		return

	def pasteItems(self):
		return

	def deleteItems(self):
		self.parent.programmeList[0].tableWidget.deleteItems()

	def deleteItemsAt(self, x, y):
		size = self.parent.programmeList[0].tableWidget.size()
		x = x + size.width()
		y = y + (size.height()/2)
		tw = self.parent.programmeList[0].tableWidget
		if tw.itemAt(x,y) == None:
			return
		row = tw.itemAt(x,y).row()
		col = tw.itemAt(x,y).column()
		tw.setItem(row,col,None)
		refreshCode(self.parent)

	def mousePressEvent(self, event):
		pm = QtGui.QPixmap(self.fileName).scaled(50,50)
		QtGui.QApplication.setOverrideCursor(QtGui.QCursor(pm))

	def mouseReleaseEvent(self, event):
		QtGui.QApplication.restoreOverrideCursor()
		if self.mode == "Delete":
			self.deleteItemsAt(event.pos().x(),event.pos().y())
		if self.mode == "Copy" and self.value is not None:
			self.pasteItems()
        	
class CustomisedTable(QtGui.QTableWidget):
	def __init__(self, parent):
        	super(CustomisedTable, self).__init__(None)
		self.parent = parent
		self.initCode = """import socket
import sys
sys.path.insert(0,\"""" + os.path.abspath("") + """\")
from robosim import *

def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('localhost', 55443))
"""
		self.endCode = """	s.close()

if __name__ == "__main__":
	main()
"""

	def dragEnterEvent(self, event):
		event.accept()

	def dropEvent(self, event):
		if(event.pos().x()>130 and self.itemAt(event.pos()) is None):
			event = QtGui.QDropEvent(QtCore.QPoint(100,event.pos().y()),event.dropAction(),event.mimeData(),event.mouseButtons(),event.keyboardModifiers(),QtCore.QEvent.Drop)

		super(CustomisedTable, self).dropEvent(event)
		refreshCode(self.parent)

	def returnCode(self):
		code = ""
		for i in range(self.rowCount()):
			if(self.item(i,0)!=None):
				code = code + "	" + self.item(i,0).whatsThis() + "\n"	
		return self.initCode + code + self.endCode

	def mousePressEvent(self,event):
		# disable clicking and selecting where there is no block
		if self.itemAt(event.pos()) == None:
			return
		else:
			super(CustomisedTable, self).mousePressEvent(event)

	def mouseDoubleClickEvent(self, event):
		if self.itemAt(event.pos()) == None:
			return
		block = self.itemAt(event.pos())
		self.blockEditor(block)

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
			if not self.currentItem() == None:
				self.blockEditor(self.currentItem())
		elif event.key() == QtCore.Qt.Key_Delete or event.key() == QtCore.Qt.Key_Backspace:
			if not self.currentItem() == None:
				self.deleteItems()		
		elif event.key() == QtCore.Qt.Key_Right:
			if self.currentItem() == None:
				return
			elif self.item(self.currentRow(),self.currentColumn()+1) == None:
				return
		else:
			super(CustomisedTable,self).keyPressEvent(event)

	def deleteItems(self):
		for i in range(self.rowCount()):
			if not self.item(i,0)==None:
				if self.item(i,0).isSelected():
					self.setItem(i,0,None)
		self.deleteNoneRows()
		refreshCode(self.parent)

	def deleteNoneRows(self):
		row = self.rowCount()
		count = 0
		while count < self.rowCount():
			if self.item(count,0)==None:
				self.removeRow(count)
			else:
				count = count + 1
		self.setRowCount(row)

	def blockEditor(self,item):
		for i in range(4):
			if i == 1:
				continue
			if item.whatsThis()[:8] == testNames[i][:8]:
				return
		newWindow = BlockEditor(item,self.parent)
		newWindow.setGeometry(QtCore.QRect(100, 100, 400, 200))
		newWindow.exec_()

class BlockEditor(QtGui.QDialog):
	def __init__(self, parent, frame):
        	super(BlockEditor, self).__init__(None)
		self.parent = parent
		self.frame = frame
		self.initUI()

	def initUI(self):
		self.paramList = [["speed","distance(motor encoder value)"]]
		self.setWindowTitle("Block Editor")
		self.text = str(self.parent.whatsThis())
		self.index = self.text.find(",")
		if self.text.find("moveForward") == 0:
			self.initForward()
		elif self.text.find("while ") == 0 or self.text.find("for ") == 0:
			self.initRepeat()
		elif self.text.find("if ") == 0 or self.text.find("else ") == 0 or self.text.find("elif ") == 0:
			self.initIfElse()
		elif self.text.find("#Edit Block") == 0:
			self.initEdit()

	def initForward(self):
		param = self.text.split(",")

		vbox = QtGui.QVBoxLayout()
		self.paramValue = []
		for i in range(len(self.paramList[0])):
			h = QtGui.QSplitter(QtCore.Qt.Horizontal)
			font = QtGui.QFont()
			font.setPixelSize(25)
			txt = QtGui.QLabel(self)
			txt.setText(self.paramList[0][i] + " = ")
			txt.setFont(font)
			edit = QtGui.QLineEdit(self)
			edit.setFont(font)
			if i == len(self.paramList[0])-1:
				edit.setText(param[i+1][:-1])
			else:
				edit.setText(param[i+1])
			self.paramValue.append(edit)
			h.addWidget(txt)
			h.addWidget(edit)
			h.setSizes([250,150])
			vbox.addWidget(h)

		#button
		h = QtGui.QSplitter(QtCore.Qt.Horizontal)
		btn = QtGui.QPushButton("OK", self)
		btn.clicked.connect(self.setValue) 
		h.addWidget(QtGui.QWidget()) #add dummy
		h.addWidget(btn)
		h.setSizes([300,100])
		vbox.addWidget(h)
		self.setLayout(vbox)

	def initRepeat(self):
		vbox = QtGui.QVBoxLayout()
		btn = QtGui.QButtonGroup(self)

		infinite = QtGui.QCheckBox("Infinite Loop",self)

		h1 = QtGui.QHBoxLayout()
		finite = QtGui.QCheckBox("Repeat for ",self)
		looptimes = QtGui.QLineEdit()
		h1_tmp = QtGui.QLabel(" times")
		h1.addWidget(finite)
		h1.addWidget(looptimes)
		h1.addWidget(h1_tmp)

		h2 = QtGui.QHBoxLayout()
		wl = QtGui.QCheckBox("while ",self)
		wls = QtGui.QLineEdit()
		h2.addWidget(wl)
		h2.addWidget(wls)
		
		h3 = QtGui.QHBoxLayout()
		fl = QtGui.QCheckBox("for ",self)
		fls = QtGui.QLineEdit()
		h3.addWidget(fl)
		h3.addWidget(fls)

		okbtn = QtGui.QPushButton("OK",self)

		btn.addButton(infinite)
		btn.addButton(finite)
		btn.addButton(wl)
		btn.addButton(fl)

		vbox.addWidget(infinite)
		vbox.addLayout(h1)
		vbox.addLayout(h2)
		vbox.addLayout(h3)
		vbox.addWidget(okbtn)

		self.setLayout(vbox)

	def initIfElse(self):
		return

	def initEdit(self):
		vbox = QtGui.QVBoxLayout()
		text = self.text.replace("\n\t","\n")[12:-19]
		self.textEdit = QtGui.QTextEdit()
		self.textEdit.setText(text)
		syntax.PythonHighlighter(self.textEdit.document())
		btn = QtGui.QPushButton("OK", self)
		btn.clicked.connect(self.setEdit)
		vbox.addWidget(self.textEdit)
		vbox.addWidget(btn)
		self.setLayout(vbox)

	def setEdit(self):
		if self.textEdit is None:
			return
		content = self.textEdit.toPlainText().replace("\n","\n\t")
		if not content[-2:] == "\n\t":
			content = content + "\n\t"
		text = "#Edit Block\n\t" + content + "#End of Edit Block"
		self.parent.setWhatsThis(text)
		refreshCode(self.frame)
		self.close()

	def setValue(self):
		values = []
		for i in range(len(self.paramValue)):
			txt = str(self.paramValue[i].text())
			if not txt.isdigit():
				reply = QtGui.QMessageBox.information(self, 'Message',"Please type in integer value", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
				if reply == QtGui.QMessageBox.Ok:
					return
			if int(txt)<0:
				reply = QtGui.QMessageBox.information(self, 'Message',"Please type in positive value", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
				if reply == QtGui.QMessageBox.Ok:
					return
			values.append(txt)

		text = self.text[:self.index]
		for i in range(len(values)):
			text = text + "," + values[i]
		text = text + ")"
		self.parent.setWhatsThis(text)
		refreshCode(self.frame)
		self.close()

def refreshCode(parent):
	tabList = parent.bottomtabList
	tabList[3].textEdit.setText(tabList[3].getText())
