#coding:utf-8

#by Teruki Tauchi

import sys
import os
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import syntax

testNames = ["flashLED()", "moveForward(s,30,300)", "setMotor(s,40,40)", "turnLeft(s)", "turnRight(s)", "setSensor(s,\"R\",-45)", "if readSensor(s,\"IFR\")<100: #Read Sensor", "if readMotorEncoder(s,\"MELR\")<1000: #Read Motor Encoder", "#Repeat Block", "#If-else block", "#Edit Block\n\t#End of Edit Block"]

class ProgrammeWindow(QtGui.QWidget):
	def __init__(self, parent):
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
		self.tableWidget.setRowCount(2)
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
			index = self.parent.screentab.currentIndex()
			value = self.parent.programmeList[index].tableWidget.returnCode()
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
		self.blockIcons = ["flash.png", "forward.png", "setmotor.png", "turnleft.png", "turnright.png", "ssensor.png", "rsensor.png", "motorencoder.png", "repeat.png", "ifelse.png", "edit.png"]
		blockNames = ["Flash LED", "Move Forward", "Set Motor (For Advanced Users)", "Turn Left", "Turn Right", "Set Sensor", "Read Sensor", "Read Motor Encoder", "Repeat", "If-Else (For Advanced Users)", "Edit (For Advanced Users)"]
	
		for i in range(len(self.blockIcons)):
			self.blockIcons[i] = "images/" + self.blockIcons[i]

		#Table for list
		hbox = QtGui.QHBoxLayout()
		self.tableList = QtGui.QTableWidget(self)
		self.tableList.setIconSize(QtCore.QSize(100,100))
		self.tableList.resize(255,300)
		self.tableList.setDragEnabled(True)
		self.tableList.setColumnCount(2)
		self.tableList.setRowCount(len(self.blockIcons))
		h = self.tableList.horizontalHeader()
		h.setDefaultSectionSize(110)
		h.setVisible(False)
		v = self.tableList.verticalHeader()
		v.setDefaultSectionSize(110)
		v.setVisible(False)
		self.tableList.setShowGrid(False)
		self.tableList.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

		for i in range(len(self.blockIcons)):
			iconItem = QtGui.QTableWidgetItem()
			icon = QtGui.QIcon(self.blockIcons[i]) 
			iconItem.setIcon(icon)
			iconItem.setSizeHint(QtCore.QSize(100,100))
			iconItem.setWhatsThis(testNames[i])
			self.tableList.setItem(i,0,iconItem)

			nameItem = QtGui.QTableWidgetItem()
			nameItem.setText(blockNames[i])
			nameItem.setFlags(QtCore.Qt.ItemIsEnabled)
			self.tableList.setItem(i,1,nameItem)

		self.tableList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
		hbox.addWidget(self.tableList)
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
		if not event.source().__class__.__name__ == "CustomisedTable":
			return
		index = self.parent.screentab.currentIndex()
		item =  self.parent.programmeList[index].tableWidget.currentItem()
		if item == None:
			return
		elif item.whatsThis() == "#End Conditional Block":
			return
		event.accept()

	def dropEvent(self, event):
		if self.mode == "Copy":
			self.copyItems()
		elif self.mode == "Delete":
			self.deleteItems()
		else:
			return

	def copyItems(self):
		index = self.parent.screentab.currentIndex()
		if self.parent.programmeList[index].tableWidget.currentItem() == None:
			return
		self.value = self.parent.programmeList[index].tableWidget.currentItem().clone()

	def pasteItems(self, x, y):
		index = self.parent.screentab.currentIndex()
		if self.value == None:
			return
		tw = self.parent.programmeList[index].tableWidget
		row = tw.rowAt(y)-1
		if row == -2 or row >= tw.rowCount()-1:
			tw.setRowCount(tw.rowCount()+1)
			row = tw.rowCount()-2
		col = tw.columnAt(x) 
		if col == 0:
			tmp = "" #do nothing
		elif tw.item(row,col) == None:
			return
		elif str(tw.item(row,col).whatsThis()).find("#End Conditional Block") == 0:
			tmp = tw.item(row,col).clone()
			if col >= tw.columnCount()-1:
				tw.setColumnCount(tw.columnCount()+1)
			tw.setItem(row,col+1,tmp)
		if str(self.value.whatsThis()).find("for ") == 0 or str(self.value.whatsThis()).find("while ") == 0 or str(self.value.whatsThis()).find("if ") == 0 or str(self.value.whatsThis()).find("elif ") == 0 or str(self.value.whatsThis()).find("else:") == 0:
			if not tw.item(row,tw.columnCount()-1) == None:
				tw.setColumnCount(tw.columnCount()+1)
			tw.putEndConditionalBlock(row,col)
		tw.setItem(row,col,self.value)
		self.value = self.value.clone()
		refreshCode(self.parent)

	def deleteItems(self):
		index = self.parent.screentab.currentIndex()
		self.parent.programmeList[index].tableWidget.deleteItems(self.parent.programmeList[index].tableWidget.currentItem())

	def deleteItemsAt(self, x, y):
		index = self.parent.screentab.currentIndex()
		tw = self.parent.programmeList[index].tableWidget
		if tw.itemAt(x,y) == None:
			return
		if str(tw.itemAt(x,y).whatsThis()).find("#End Conditional Block") == 0:
			return
		tw.deleteItems(tw.itemAt(x,y))

	def mousePressEvent(self, event):
		pm = QtGui.QPixmap(self.fileName).scaled(50,50)
		QtGui.QApplication.setOverrideCursor(QtGui.QCursor(pm))

	def mouseReleaseEvent(self, event):
		index = self.parent.screentab.currentIndex()
		QtGui.QApplication.restoreOverrideCursor()
		size = self.parent.programmeList[index].tableWidget.size()
		x = event.pos().x() + size.width()
		y = event.pos().y() + (size.height()/2)
		if self.mode == "Delete":
			self.deleteItemsAt(x,y)
		if self.mode == "Copy" and self.value is not None:
			self.pasteItems(x,y)
        	
class CustomisedTable(QtGui.QTableWidget):
	def __init__(self, parent):
        	super(CustomisedTable, self).__init__(None)
		self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		self.parent = parent
		self.initCode = """import socket
import sys
sys.path.insert(0,\"""" + os.path.abspath("") + """\")
from robosim import *

def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#s = serial.Serial("COM1", 9600)
	s.connect(('localhost', 55443))
"""
		self.endCode = """	s.close()

if __name__ == "__main__":
	main()
"""

	def dragEnterEvent(self, event):
		if event.source().__class__.__name__ == "CustomisedTable":
			return
			# We won't accept drag and drop from itself
		event.accept()

	def dropEvent(self, event):
		if self.columnAt(event.pos().x()) == self.columnCount()-1:
			self.setColumnCount(self.columnCount()+1)
		leftCol = self.columnAt(0)
		if not leftCol == 0:
			if leftCol == -1:
				return
			itm = self.item(self.rowAt(event.pos().y()),leftCol-1)
			if itm == None:
				return
			itmtxt = str(itm.whatsThis())
			if leftCol == 1:
				isConditional = itmtxt.find("while ") == 0 or itmtxt.find("for ") == 0 or itmtxt.find("#Repeat Block") == 0 or itmtxt.find("if ") == 0 or itmtxt.find("elif ") == 0 or itmtxt.find("else:") == 0 or itmtxt.find("#If-else") == 0
				if not isConditional:
					return
			#elif itmtxt.find("#End Conditional Block") == 0:
				#return

		col = self.columnAt(event.pos().x())
		row = self.rowAt(event.pos().y())
		if not self.item(row,col) == None:
			tmpBlock = str(self.item(row,col).whatsThis())
			blockIsConditional = tmpBlock.find("while ") == 0 or tmpBlock.find("for ") == 0 or tmpBlock.find("#Repeat Block") == 0 or tmpBlock.find("if ") == 0 or tmpBlock.find("elif ") == 0 or tmpBlock.find("else:") == 0 or tmpBlock.find("#If-else") == 0
			if blockIsConditional:
				return
		if row >= self.rowCount()-1:
			self.setRowCount(self.rowCount()+1)
		if self.item(row,0) == None:
			event = QtGui.QDropEvent(QtCore.QPoint(0,event.pos().y()),event.dropAction(),event.mimeData(),event.mouseButtons(),event.keyboardModifiers(),QtCore.QEvent.Drop)
			super(CustomisedTable, self).dropEvent(event)
			refreshCode(self.parent)
			return
		leftBlock = str(self.item(row,0).whatsThis())
		leftBlockIsConditional = leftBlock.find("while ") == 0 or leftBlock.find("for ") == 0 or leftBlock.find("#Repeat Block") == 0 or leftBlock.find("if ") == 0 or leftBlock.find("elif ") == 0 or leftBlock.find("else:") == 0 or leftBlock.find("#If-else") == 0
		if col == 0 and leftBlockIsConditional:
			return
		elif not leftBlockIsConditional:
			if not col == 0:
				event = QtGui.QDropEvent(QtCore.QPoint(0,event.pos().y()),event.dropAction(),event.mimeData(),event.mouseButtons(),event.keyboardModifiers(),QtCore.QEvent.Drop)
			super(CustomisedTable, self).dropEvent(event)
			refreshCode(self.parent)
			return
		elif col == 1 and self.item(row,col+1)==None:
			tmpItem = QtGui.QTableWidgetItem()
			iconFileName = ""
			if not leftBlock.find("#Read Sensor") == -1:
				iconFileName = "images/rsensor_s.png"
			elif not leftBlock.find("#Read Motor Encoder") == -1:
				iconFileName = "images/motorencoder_s.png"
			elif leftBlock.find("while ") == 0 or leftBlock.find("for ") == 0 or leftBlock.find("#Repeat Block") == 0:
				iconFileName = "images/repeat_s.png"
			elif leftBlock.find("if ") == 0 or leftBlock.find("elif ") == 0 or leftBlock.find("else:") == 0 or leftBlock.find("#If-else") == 0:
				iconFileName = "images/ifelse_s.png"
			tmpIcon = QtGui.QIcon(iconFileName) 
			tmpItem.setIcon(tmpIcon)
			tmpItem.setSizeHint(QtCore.QSize(100,100))
			if leftBlock == "#Repeat Block":
				leftBlock = "while True:" #default value
			elif leftBlock == "#If-else block":
				leftBlock = "if True:" #default value
			tmpItem.setWhatsThis(leftBlock)
			#tmpItem.setFlags(QtCore.Qt.ItemIsEnabled)
			self.setItem(row,0,tmpItem)
			self.putEndConditionalBlock(row,col)
			super(CustomisedTable, self).dropEvent(event)
			refreshCode(self.parent)
		leftShift = 0
		if leftBlockIsConditional and col > 1 and self.item(row,col) == None:
			return
			commentout = """
		#if leftBlockIsConditional and col > 1 and str(self.item(row,col).whatsThis()).find("#End Conditional Block") == 0:
			#col = col - 1
		if leftBlockIsConditional and not leftShift == 0:
			val = event.pos().x() - (130*leftShift)
			if val<0:
				val = 0
			event = QtGui.QDropEvent(QtCore.QPoint(val,event.pos().y()),event.dropAction(),event.mimeData(),event.mouseButtons(),event.keyboardModifiers(),QtCore.QEvent.Drop)	"""
		if str(self.itemAt(event.pos().x(),event.pos().y()).whatsThis()).find("#End Conditional Block") == 0:
			self.putEndConditionalBlock(row,col)

		super(CustomisedTable, self).dropEvent(event)
		if col >= 1:
			iconFileName = "null"
			iconWhatsThis = ""
			if str(event.source().currentItem().whatsThis()) == testNames[8]:
				iconFileName = "images/repeat_s.png"
				iconWhatsThis = "while True:"
			elif str(event.source().currentItem().whatsThis()) == testNames[6]:
				iconFileName = "images/rsensor_s.png"
				iconWhatsThis = testNames[6]
			elif str(event.source().currentItem().whatsThis()) == testNames[7]:
				iconFileName = "images/motorencoder_s.png"
				iconWhatsThis = testNames[7]
			elif str(event.source().currentItem().whatsThis()) == testNames[9]:
				iconFileName = "images/ifelse_s.png"
				iconWhatsThis = "if True:"
			if iconFileName.find("null")==-1:
				tmpItem = QtGui.QTableWidgetItem()
				tmpIcon = QtGui.QIcon(iconFileName) 
				tmpItem.setIcon(tmpIcon)
				tmpItem.setSizeHint(QtCore.QSize(100,100))
				tmpItem.setWhatsThis(iconWhatsThis)
				#tmpItem.setFlags(QtCore.Qt.ItemIsEnabled)
				self.setItem(row,col,tmpItem)
				if not self.item(row,self.columnCount()-1) == None:
					self.setColumnCount(self.columnCount()+1)
				self.putEndConditionalBlock(row,col)

		refreshCode(self.parent)

	def putEndConditionalBlock(self,row,col):
		tr = row
		tc = col + 1
		if not self.item(tr,tc) == None:
			tmpVal1 = self.item(tr,tc).clone()
			while not self.item(tr,tc)==None:
				tmpVal2 = None
				if tc+1 >= self.columnCount():
					self.setColumnCount(self.columnCount()+1)
				if not self.item(tr,tc+1) == None:
					tmpVal2 = self.item(tr,tc+1).clone()
				self.setItem(tr,tc+1,tmpVal1)
				tmpVal1 = tmpVal2
				tc = tc + 1

		i = col + 1
		iconFileName = ""
		numClose = 0
		while i >= 0:
			if self.item(row,i)==None:
				i = i - 1
			elif str(self.item(row,i).whatsThis()).find("#End Conditional Block")==0:
				numClose = numClose + 1
				i = i - 1
			elif (not str(self.item(row,i).whatsThis()).find("#Read Sensor") == -1):
				if numClose <= 0:
					iconFileName = "images/rsensor_e.png"
					break
				else:
					numClose = numClose - 1
			elif (not str(self.item(row,i).whatsThis()).find("#Read Motor Encoder") == -1):
				if numClose <= 0:
					iconFileName = "images/motorencoder_e.png"
					break
				else:
					numClose = numClose - 1
			elif (str(self.item(row,i).whatsThis()).find("for ") == 0 or str(self.item(row,i).whatsThis()).find("while ") == 0):
				if numClose <= 0:
					iconFileName = "images/repeat_e.png"
					break
				else:
					numClose = numClose - 1
			elif (str(self.item(row,i).whatsThis()).find("if ") == 0 or str(self.item(row,i).whatsThis()).find("elif ") == 0 or str(self.item(row,i).whatsThis()).find("else:") == 0):
				if numClose <= 0:
					iconFileName = "images/ifelse_e.png"
					break
				else:
					numClose = numClose - 1
			else:
				i = i - 1

		tmpItem = QtGui.QTableWidgetItem()
		tmpIcon = QtGui.QIcon(iconFileName) 
		tmpItem.setIcon(tmpIcon)
		tmpItem.setSizeHint(QtCore.QSize(100,100))
		tmpItem.setWhatsThis("#End Conditional Block")
		#tmpItem.setFlags(QtCore.Qt.ItemIsEnabled)
		self.setItem(row,col+1,tmpItem)

	def returnCode(self):
		code = ""
		for i in range(self.rowCount()):
			if(self.item(i,0)!=None):
				itemText = str(self.item(i,0).whatsThis())
				isCondition = itemText.find("for ")==0 or itemText.find("while ")==0 or itemText.find("if ")==0 or itemText.find("elif ")==0 or itemText.find("else:")==0
				if isCondition:
					itemText = self.conditionalStatement(i,0,2)
				code = code + "	" + itemText + "\n"	
		return self.initCode + code.replace("\n\n","\n") + self.endCode
		# There is a weird bug that the generated code sometimes has lines without any code. I don't know the reason yet, but I am using replace("\n\n","\n") for now to fix this problem

	def conditionalStatement(self, row, col, numTabs):
		tab = "\n"
		for i in range(numTabs):
			tab = tab + "\t"
		text = str(self.item(row,col).whatsThis())
		if self.item(row,col+1) == None:
			return text + tab + "break"
		elif str(self.item(row,col+1).whatsThis()).find("#End Conditional Block")==0:
			return text + tab + "break"

		count = 1
		item = self.item(row,col+count)
		while not item == None:
			tmp = str(item.whatsThis())
			if tmp.find("for ") == 0 or tmp.find("while ") == 0 or tmp.find("if ") == 0 or tmp.find("elif ") == 0 or tmp.find("else:") == 0:
				tmp = self.conditionalStatement(row,col+count,numTabs+1)
				tmpBlacket = 0
				while (not str(self.item(row,col+count).whatsThis()).find("#End Conditional Block")==0) or tmpBlacket > 1:
					tmpTxt = str(self.item(row,col+count).whatsThis())
					if tmpTxt.find("for ") == 0 or tmpTxt.find("while ") == 0 or tmpTxt.find("if ") == 0 or tmpTxt.find("elif ") == 0 or tmpTxt.find("else:") == 0:
						tmpBlacket = tmpBlacket + 1
					elif tmpTxt.find("#End Conditional Block")==0:
						tmpBlacket = tmpBlacket - 1
					count = count + 1
					if self.item(row,col+count) == None:
						break
			elif tmp.find("#Edit Block")==0:
				tmp = tmp.replace("\n\t",tab)				
			elif tmp.find("#End Conditional Block")==0:
				return text
			text = text + tab + tmp
			count = count + 1
			item = self.item(row,col+count)
		return text

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
				self.deleteItems(self.currentItem())		
		elif event.key() == QtCore.Qt.Key_Right:
			if self.currentItem() == None:
				return
			elif self.item(self.currentRow(),self.currentColumn()+1) == None:
				return
			else:
				super(CustomisedTable,self).keyPressEvent(event)
		else:
			super(CustomisedTable,self).keyPressEvent(event)

	def deleteItems(self,item):
		row = item.row()
		col = item.column()
		isConditionalBlock = str(item.whatsThis()).find("while ")==0 or str(item.whatsThis()).find("for ")==0 or str(item.whatsThis()).find("if ")==0 or str(item.whatsThis()).find("elif ")==0 or str(item.whatsThis()).find("else:")==0
		self.setItem(row,col,None)
		if col == 0:
			self.removeRow(row)
			self.setRowCount(self.rowCount()+1)
			self.verticalScrollBar().setSliderPosition(0)
		else:
			next = col + 1
			while not self.item(row,next)==None:
				if next == self.columnCount():
					break
				itm = self.item(row,next).clone()
				self.setItem(row,next-1,itm)
				next = next + 1
			self.setItem(row,next-1,None)
			if isConditionalBlock:
				while True:
					item = self.item(row,col)
					if item == None:
						break
					if str(item.whatsThis()).find("#End Conditional Block")==0:
						self.deleteItems(item)
						break
					self.deleteItems(item)
		refreshCode(self.parent)
		commentout = """
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
		self.setRowCount(row)"""

	def blockEditor(self,item):
		for i in range(5):
			if i == 1 or i == 2:
				continue
			if item.whatsThis()[:8] == testNames[i][:8]:
				return
		newWindow = BlockEditor(item,self.parent)
		newWindow.setGeometry(QtCore.QRect(100, 100, 400, 200))
		newWindow.exec_()

class BlockEditor(QtGui.QDialog):
	def __init__(self, item, parent):
        	super(BlockEditor, self).__init__(None)
		self.item = item
		self.parent = parent
		self.initUI()

	def initUI(self):
		self.paramList = [["speed","distance(motor encoder value)"],["left motor","right motor"]]
		self.setWindowTitle("Block Editor")
		self.text = str(self.item.whatsThis())
		self.index = self.text.find(",")
		if self.text.find("#Edit Block") == 0:
			self.initEdit()
		elif self.text.find("moveForward(") == 0:
			self.initForward()
		elif not self.text.find("#Read Sensor") == -1:
			self.initReadSensor()
		elif not self.text.find("#Read Motor Encoder") == -1:
			self.initMotorEncoder()
		elif self.text.find("setMotor(") == 0:
			self.initSetMotor()
		elif self.text.find("setSensor(") == 0:
			self.initSetSensor()
		elif self.text.find("while ") == 0 or self.text.find("for ") == 0 or self.text.find(testNames[8]) == 0:
			self.initRepeat()
		elif self.text.find("if ") == 0 or self.text.find("else:") == 0 or self.text.find("elif ") == 0 or self.text.find(testNames[9]) == 0:
			self.initIfElse()

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

	def initSetMotor(self):
		param = self.text.split(",")

		vbox = QtGui.QVBoxLayout()
		caution = QtGui.QLabel("Set Motor is not recommended for beginner.\nPlease use Move Forward Block instead where possible",self)
		vbox.addWidget(caution)
		self.paramValue = []
		for i in range(len(self.paramList[1])):
			h = QtGui.QSplitter(QtCore.Qt.Horizontal)
			font = QtGui.QFont()
			font.setPixelSize(25)
			txt = QtGui.QLabel(self)
			txt.setText(self.paramList[1][i] + " = ")
			txt.setFont(font)
			edit = QtGui.QLineEdit(self)
			edit.setFont(font)
			if i == len(self.paramList[1])-1:
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
		
		self.looptimes = QtGui.QLineEdit()
		h1_tmp = QtGui.QLabel(" times")
		h1.addWidget(finite)
		h1.addWidget(self.looptimes)
		h1.addWidget(h1_tmp)

		caution = QtGui.QLabel("\nOptions below are not recommended for beginners",self)

		h2 = QtGui.QHBoxLayout()
		wl = QtGui.QCheckBox("while ",self)
		self.wls = QtGui.QLineEdit()
		h2.addWidget(wl)
		h2.addWidget(self.wls)
		
		h3 = QtGui.QHBoxLayout()
		fl = QtGui.QCheckBox("for ",self)
		self.fls = QtGui.QLineEdit()
		h3.addWidget(fl)
		h3.addWidget(self.fls)

		okbtn = QtGui.QPushButton("OK",self)
		okbtn.clicked.connect(self.setRepeat)

		if self.text.find("while True:") == 0:
			infinite.setChecked(True)
		elif self.text.find("for ") == 0 and not self.text.find("in range(") == -1:
			finite.setChecked(True)
			self.looptimes.setText(self.text[self.text.find("in range(")+9:-2])
		elif self.text.find("while ") == 0:
			wl.setChecked(True)
			self.wls.setText(self.text[6:])
		elif self.text.find("for ") == 0:
			fl.setChecked(True)
			self.fls.setText(self.text[4:])
		self.repeatCheck = [infinite, finite, wl, fl]

		btn.addButton(infinite)
		btn.addButton(finite)
		btn.addButton(wl)
		btn.addButton(fl)

		vbox.addWidget(infinite)
		vbox.addLayout(h1)
		vbox.addWidget(caution)
		vbox.addLayout(h2)
		vbox.addLayout(h3)
		vbox.addWidget(okbtn)

		self.setLayout(vbox)

	def setRepeat(self):
		index = self.parent.screentab.currentIndex()
		if self.repeatCheck == None:
			return
		if self.repeatCheck[0].checkState():
			self.item.setWhatsThis("while True:")
		elif self.repeatCheck[1].checkState():
			val = str(self.looptimes.text()).strip()
			if not val.isdigit():
				reply = QtGui.QMessageBox.information(self, 'Message',"Please type in natural number value", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
				if reply == QtGui.QMessageBox.Ok:
					return
			col = self.parent.programmeList[index].tableWidget.currentColumn()
			self.item.setWhatsThis("for i" + str(col) + " in range(" + val + "):")
		elif self.repeatCheck[2].checkState():
			txt = "while " + str(self.wls.text())
			if not txt[-1:] == ":":
				txt = txt + ":"
			self.item.setWhatsThis(txt)
		elif self.repeatCheck[3].checkState():
			txt = "for " + str(self.fls.text())
			if not txt[-1:] == ":":
				txt = txt + ":"
			self.item.setWhatsThis(txt)
		else:
			self.close()

		refreshCode(self.parent)
		self.close()		

	def initIfElse(self):
		vbox = QtGui.QVBoxLayout()
		btn = QtGui.QButtonGroup(self)

		caution = QtGui.QLabel("If-Else Block is not recommended for beginners.\nPlease use Read Sensor or Read Motor Encoder Block instead.\nWhen using If-Else Block,\ndon't forget to put if block before elif and else!")

		h1 = QtGui.QHBoxLayout()
		ifCheck = QtGui.QCheckBox("if ",self)
		ifStatement = QtGui.QLineEdit()
		if self.text.find("if ") == 0:
			ifCheck.setChecked(True)
			ifStatement.setText(self.text[3:])
		h1.addWidget(ifCheck)
		h1.addWidget(ifStatement)

		h2 = QtGui.QHBoxLayout()
		elifCheck = QtGui.QCheckBox("elif ",self)
		elifStatement = QtGui.QLineEdit()
		if self.text.find("elif ") == 0:
			elifCheck.setChecked(True)
			elifStatement.setText(self.text[5:])
		h2.addWidget(elifCheck)
		h2.addWidget(elifStatement)

		elseCheck = QtGui.QCheckBox("else:",self)
		if self.text.find("else:") == 0:
			elseCheck.setChecked(True)

		btn.addButton(ifCheck)
		btn.addButton(elifCheck)
		btn.addButton(elseCheck)
		self.ifElseCheck = [ifCheck,elifCheck,elseCheck]
		self.ifElseStatement = [ifStatement,elifStatement]

		vbox.addWidget(caution)
		vbox.addLayout(h1)
		vbox.addLayout(h2)
		vbox.addWidget(elseCheck)

		okButton = QtGui.QPushButton("OK",self)
		okButton.clicked.connect(self.setIfElse)
		vbox.addWidget(okButton)

		self.setLayout(vbox)

	def setIfElse(self):
		if self.ifElseCheck == None or self.ifElseStatement == None:
			return
		ifElse = ["if ","elif ","else:"]
		isExecuted = False
		if self.ifElseCheck[2].checkState():
			self.item.setWhatsThis("else:")
			refreshCode(self.parent)
			self.close()
			return
		for i in range(2):
			if self.ifElseCheck[i].checkState():
				isExecuted = True
				if str(self.ifElseStatement[i].text()).strip() == "":
					reply = QtGui.QMessageBox.information(self, 'Message',"Please type in something", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
					if reply == QtGui.QMessageBox.Ok:
						return
				txt = ifElse[i] + str(self.ifElseStatement[i].text())
				if not txt[-1:] == ":":
					txt = txt + ":"
				self.item.setWhatsThis(txt)
		if not isExecuted:
			return
		else:
			refreshCode(self.parent)
			self.close()

	def initReadSensor(self):
		self.availableReadSensorNames = ["Front Right Infrared Sensor","Front Left Infrared Sensor","Side Right Inrared Sensor","Side Left Infrared Sensor","UltraSound"]
		self.availableReadSensor = ["IFR","IFL","ISR","ISL","US"]
		vbox = QtGui.QVBoxLayout()
		self.readSensor = []
		
		ifOrWhile = QtGui.QButtonGroup(self)
		ifCheck = QtGui.QCheckBox("Execute only once",self)
		whileCheck = QtGui.QCheckBox("Repeat",self)
		ifOrWhile.addButton(ifCheck)
		ifOrWhile.addButton(whileCheck)
		self.readSensor.append(ifCheck)
		self.readSensor.append(whileCheck)
		vbox.addWidget(ifCheck)
		vbox.addWidget(whileCheck)
		if self.text.find("if ")==0:
			ifCheck.setChecked(True)
		elif self.text.find("while ")==0:
			whileCheck.setChecked(True)

		chooseSensor = QtGui.QLabel("Choose Sensor",self)
		vbox.addWidget(chooseSensor)
		self.selectReadSensor = QtGui.QComboBox(self)
		for i in range(len(self.availableReadSensorNames)):
			self.selectReadSensor.addItem(self.availableReadSensorNames[i])
			if not self.text.find(self.availableReadSensor[i])==-1:
				self.selectReadSensor.setCurrentIndex(i)
		vbox.addWidget(self.selectReadSensor)

		nearOrFar = QtGui.QButtonGroup(self)
		h1 = QtGui.QHBoxLayout()
		nearCheck = QtGui.QCheckBox("Nearer than ",self)
		self.readSensorNearer = QtGui.QLineEdit(self)
		unit = QtGui.QLabel("cm (approximately)",self)
		h1.addWidget(nearCheck)
		h1.addWidget(self.readSensorNearer)
		h1.addWidget(unit)
		vbox.addLayout(h1)
		h2 = QtGui.QHBoxLayout()
		farCheck = QtGui.QCheckBox("Further than ",self)
		self.readSensorFurther = QtGui.QLineEdit(self)
		unit2 = QtGui.QLabel("cm (approximately)",self)
		h2.addWidget(farCheck)
		h2.addWidget(self.readSensorFurther)
		h2.addWidget(unit2)
		vbox.addLayout(h2)
		nearOrFar.addButton(nearCheck)
		nearOrFar.addButton(farCheck)
		if not self.text.find("<")==-1:
			nearCheck.setChecked(True)
			self.readSensorNearer.setText(self.text[self.text.index("<")+1:self.text.index(":")])
		elif not self.text.find(">")==-1:
			farCheck.setChecked(True)
			self.readSensorFurther.setText(self.text[self.text.index(">")+1:self.text.index(":")])
		self.readSensor.append(nearCheck)
		self.readSensor.append(farCheck)

		okButton = QtGui.QPushButton("Ok",self)
		okButton.clicked.connect(self.setReadSensor)
		vbox.addWidget(okButton)

		self.setLayout(vbox)

	def setReadSensor(self):
		if self.readSensor == None:
			return
		txt = ""
		if self.readSensor[0].checkState():
			txt = "if readSensor(s,\""
		elif self.readSensor[1].checkState():
			txt = "while readSensor(s,\""
		else:
			return
		txt = txt + self.availableReadSensor[self.selectReadSensor.currentIndex()]
		if self.readSensor[2].checkState():
			val = str(self.readSensorNearer.text()).strip()
			if not val.isdigit():
				reply = QtGui.QMessageBox.information(self, 'Message',"Please type in natural number value", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
				if reply == QtGui.QMessageBox.Ok:
					return
			txt = txt + "\")<" + val
		elif self.readSensor[3].checkState():
			val = str(self.readSensorFurther.text()).strip()
			if not val.isdigit():
				reply = QtGui.QMessageBox.information(self, 'Message',"Please type in natural number value", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
				if reply == QtGui.QMessageBox.Ok:
					return
			txt = txt + "\")>" + val
		else:
			return
		txt = txt + ": #Read Sensor"
		
		self.item.setWhatsThis(txt)
		refreshCode(self.parent)
		self.close()

	def initSetSensor(self):
		self.availableSetSensorNames = ["Front Right Infrared Sensor","Front Left Infrared Sensor"]
		self.availableSetSensor = ["R","L"]
		vbox = QtGui.QVBoxLayout()

		chooseSensor = QtGui.QLabel("Choose Sensor",self)
		vbox.addWidget(chooseSensor)
		self.selectSetSensor = QtGui.QComboBox(self)
		for i in range(len(self.availableSetSensorNames)):
			self.selectSetSensor.addItem(self.availableSetSensorNames[i])
			if not self.text.find(self.availableSetSensor[i])==-1:
				self.selectSetSensor.setCurrentIndex(i)
		vbox.addWidget(self.selectSetSensor)

		setSensorValue = QtGui.QLabel("Set Sensor Value (e.g. -45)",self)
		vbox.addWidget(setSensorValue)

		self.setSensor = QtGui.QLineEdit(self)
		vbox.addWidget(self.setSensor)
		self.setSensor.setText(self.text[self.text.index("\",")+2:self.text.index(")")])

		okButton = QtGui.QPushButton("Ok",self)
		okButton.clicked.connect(self.setSetSensor)
		vbox.addWidget(okButton)

		self.setLayout(vbox)

	def setSetSensor(self):
		if self.setSensor == None:
			return
		val = str(self.setSensor.text()).strip()
		if val == "":
			reply = QtGui.QMessageBox.information(self, 'Message',"Please type in value", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
			if reply == QtGui.QMessageBox.Ok:
				return
		txt = "setSensor(s,\"" + self.availableSetSensor[self.selectSetSensor.currentIndex()] + "\"," + val + ")"

		self.item.setWhatsThis(txt)
		refreshCode(self.parent)
		self.close()

	def initMotorEncoder(self):
		self.availableMotorEncoderNames = ["Average of the two motor encoders","Right motor encoder","Left motor encoder"]
		self.availableMotorEncoder = ["MELR","MER","MEL"]
		vbox = QtGui.QVBoxLayout()
		self.motorEncoder = []
		
		ifOrWhile = QtGui.QButtonGroup(self)
		ifCheck = QtGui.QCheckBox("Execute only once",self)
		whileCheck = QtGui.QCheckBox("Repeat",self)
		ifOrWhile.addButton(ifCheck)
		ifOrWhile.addButton(whileCheck)
		self.motorEncoder.append(ifCheck)
		self.motorEncoder.append(whileCheck)
		vbox.addWidget(ifCheck)
		vbox.addWidget(whileCheck)
		if self.text.find("if ")==0:
			ifCheck.setChecked(True)
		elif self.text.find("while ")==0:
			whileCheck.setChecked(True)

		chooseMotor = QtGui.QLabel("Choose Motor Encoder",self)
		vbox.addWidget(chooseMotor)
		self.selectMotorEncoder = QtGui.QComboBox(self)
		for i in range(len(self.availableMotorEncoderNames)):
			self.selectMotorEncoder.addItem(self.availableMotorEncoderNames[i])
		if not self.text.find(self.availableMotorEncoder[0])==-1:
			self.selectMotorEncoder.setCurrentIndex(0)
		elif not self.text.find(self.availableMotorEncoder[1])==-1:
			self.selectMotorEncoder.setCurrentIndex(1)
		elif not self.text.find(self.availableMotorEncoder[2])==-1:
			self.selectMotorEncoder.setCurrentIndex(2)
		vbox.addWidget(self.selectMotorEncoder)

		lessMore = QtGui.QButtonGroup(self)
		h1 = QtGui.QHBoxLayout()
		lessCheck = QtGui.QCheckBox("Less than ",self)
		self.motorEncoderLessThan = QtGui.QLineEdit(self)
		unit = QtGui.QLabel("encoder ticks",self)
		h1.addWidget(lessCheck)
		h1.addWidget(self.motorEncoderLessThan)
		h1.addWidget(unit)
		vbox.addLayout(h1)
		h2 = QtGui.QHBoxLayout()
		moreCheck = QtGui.QCheckBox("More than ",self)
		self.motorEncoderMoreThan = QtGui.QLineEdit(self)
		unit2 = QtGui.QLabel("encoder ticks",self)
		h2.addWidget(moreCheck)
		h2.addWidget(self.motorEncoderMoreThan)
		h2.addWidget(unit2)
		vbox.addLayout(h2)
		lessMore.addButton(lessCheck)
		lessMore.addButton(moreCheck)
		if not self.text.find("<")==-1:
			lessCheck.setChecked(True)
			self.motorEncoderLessThan.setText(self.text[self.text.index("<")+1:self.text.index(":")])
		elif not self.text.find(">")==-1:
			moreCheck.setChecked(True)
			self.motorEncoderMoreThan.setText(self.text[self.text.index(">")+1:self.text.index(":")])
		self.motorEncoder.append(lessCheck)
		self.motorEncoder.append(moreCheck)

		okButton = QtGui.QPushButton("Ok",self)
		okButton.clicked.connect(self.setMotorEncoder)
		vbox.addWidget(okButton)

		self.setLayout(vbox)

	def setMotorEncoder(self):
		if self.motorEncoder == None:
			return
		txt = ""
		if self.motorEncoder[0].checkState():
			txt = "if readMotorEncoder(s,\""
		elif self.motorEncoder[1].checkState():
			txt = "while readMotorEncoder(s,\""
		else:
			return
		txt = txt + self.availableMotorEncoder[self.selectMotorEncoder.currentIndex()]
		if self.motorEncoder[2].checkState():
			val = str(self.motorEncoderLessThan.text()).strip()
			if val == "":
				reply = QtGui.QMessageBox.information(self, 'Message',"Please type in value", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
				if reply == QtGui.QMessageBox.Ok:
					return
			txt = txt + "\")<" + val
		elif self.motorEncoder[3].checkState():
			val = str(self.motorEncoderMoreThan.text()).strip()
			if val == "":
				reply = QtGui.QMessageBox.information(self, 'Message',"Please type in value", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
				if reply == QtGui.QMessageBox.Ok:
					return
			txt = txt + "\")>" + val
		else:
			return
		txt = txt + ": #Read Motor Encoder"
		
		self.item.setWhatsThis(txt)
		refreshCode(self.parent)
		self.close()

	def initEdit(self):
		vbox = QtGui.QVBoxLayout()
		text = self.text.replace("\n\t","\n")[12:-19]
		self.textEdit = QtGui.QTextEdit()
		self.textEdit.setText(text)
		syntax.PythonHighlighter(self.textEdit.document())
		hbox = QtGui.QHBoxLayout()
		btn = QtGui.QPushButton("OK", self)
		btn.clicked.connect(self.setEdit)
		sav = QtGui.QPushButton("Save", self)
		sav.clicked.connect(self.saveEdit)
		hbox.addWidget(btn)
		hbox.addWidget(sav)
		vbox.addWidget(self.textEdit)
		vbox.addLayout(hbox)
		self.setLayout(vbox)

	def setEdit(self):
		if self.textEdit is None:
			return
		content = self.textEdit.toPlainText().replace("\n","\n\t")
		if not content[-2:] == "\n\t":
			content = content + "\n\t"
		text = "#Edit Block\n\t" + content + "#End of Edit Block"
		self.item.setWhatsThis(text)
		refreshCode(self.parent)
		self.close()

	def saveEdit(self):
		if self.textEdit is None:
			return
		fileName = QtGui.QFileDialog.getSaveFileName()
		if not fileName.isEmpty():
			content = self.textEdit.toPlainText().replace("\n","\n\t")
			if not content[-2:] == "\n\t":
				content = content + "\n"
			else:
				content = content[:-1]
			f = file(fileName, "w")
			content = CustomisedTable(None).initCode + "\t" + content + CustomisedTable(None).endCode
			f.write(content)

	def setValue(self):
		values = []
		for i in range(len(self.paramValue)):
			txt = str(self.paramValue[i].text()).strip()
			commentout = """if not txt.isdigit():
				reply = QtGui.QMessageBox.information(self, 'Message',"Please type in natural number value", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
				if reply == QtGui.QMessageBox.Ok:
					return"""
			values.append(txt)

		text = self.text[:self.index]
		for i in range(len(values)):
			text = text + "," + values[i]
		text = text + ")"
		self.item.setWhatsThis(text)
		refreshCode(self.parent)
		self.close()

def refreshCode(parent):
	tabList = parent.bottomtabList
	tabList[3].textEdit.setText(tabList[3].getText())
	index = parent.screentab.currentIndex()
	tw = parent.programmeList[index].tableWidget
	i = 0
	while tw.item(0,0) == None:
		tw.removeRow(0)
		i = i + 1
		if i > 10000:
			return
	tw.setRowCount(tw.rowCount()+i)
