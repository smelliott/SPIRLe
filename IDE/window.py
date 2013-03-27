#coding:utf-8

#by Teruki Tauchi

import sys
import os
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import syntax

testNames = ["flashLED()", "moveForward(s,30,300)", "turnLeft(s)", "turnRight(s)", "#Repeat Block", "#If-else block", "#Edit Block\n\t#End of Edit Block"]

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
		blockIcons = ["flash.png", "forward.png", "turnleft.png", "turnright.png", "repeat.png", "ifelse.png", "edit.png"]
		blockNames = ["Flash LED", "Move Forward", "Turn Left", "Turn Right", "Repeat", "If-Else", "Edit"]
	
		for i in range(len(blockIcons)):
			blockIcons[i] = "images/" + blockIcons[i]

		#Table for list
		hbox = QtGui.QHBoxLayout()
		self.tableList = QtGui.QTableWidget(self)
		self.tableList.setIconSize(QtCore.QSize(100,100))
		self.tableList.resize(255,300)
		self.tableList.setDragEnabled(True)
		self.tableList.setColumnCount(2)
		self.tableList.setRowCount(len(blockIcons))
		h = self.tableList.horizontalHeader()
		h.setDefaultSectionSize(110)
		h.setVisible(False)
		v = self.tableList.verticalHeader()
		v.setDefaultSectionSize(110)
		v.setVisible(False)
		self.tableList.setShowGrid(False)
		self.tableList.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

		for i in range(len(blockIcons)):
			iconItem = QtGui.QTableWidgetItem()
			icon = QtGui.QIcon(blockIcons[i]) 
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
		elif item.whatsThis() == "#End Repeat Block":
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
		elif str(tw.item(row,col).whatsThis()).find("#End Repeat Block") == 0:
			tmp = tw.item(row,col).clone()
			if col >= tw.columnCount()-1:
				tw.setColumnCount(tw.columnCount()+1)
			tw.setItem(row,col+1,tmp)
		if str(self.value.whatsThis()).find("for ") == 0 or str(self.value.whatsThis()).find("while ") == 0:
			if not tw.item(row,tw.columnCount()-1) == None:
				tw.setColumnCount(tw.columnCount()+1)
			tw.putEndRepeatBlock(row,col)
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
		if str(tw.itemAt(x,y).whatsThis()).find("#End Repeat Block") == 0:
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
				isConditional = itmtxt.find("while ") == 0 or itmtxt.find("for ") == 0 or itmtxt.find("#Repeat Block") == 0
				if not isConditional:
					return
			elif itmtxt.find("#End Repeat Block") == 0:
				return

		col = self.columnAt(event.pos().x())
		row = self.rowAt(event.pos().y())
		if row >= self.rowCount()-1:
			self.setRowCount(self.rowCount()+1)
		if self.item(row,0) == None:
			event = QtGui.QDropEvent(QtCore.QPoint(0,event.pos().y()),event.dropAction(),event.mimeData(),event.mouseButtons(),event.keyboardModifiers(),QtCore.QEvent.Drop)
			super(CustomisedTable, self).dropEvent(event)
			refreshCode(self.parent)
			return
		leftBlock = str(self.item(row,0).whatsThis())
		leftBlockIsConditional = leftBlock.find("while ") == 0 or leftBlock.find("for ") == 0 or leftBlock.find("#Repeat Block") == 0
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
			tmpIcon = QtGui.QIcon("images/repeat_s.png") 
			tmpItem.setIcon(tmpIcon)
			tmpItem.setSizeHint(QtCore.QSize(100,100))
			if leftBlock == "#Repeat Block":
				leftBlock = "while True:" #default value
			tmpItem.setWhatsThis(leftBlock)
			#tmpItem.setFlags(QtCore.Qt.ItemIsEnabled)
			self.setItem(row,0,tmpItem)
			self.putEndRepeatBlock(row,col)
			super(CustomisedTable, self).dropEvent(event)
			refreshCode(self.parent)
			return
		leftShift = 0
		if leftBlockIsConditional and col > 1 and self.item(row,col) == None:
			return
			commentout = """
		#if leftBlockIsConditional and col > 1 and str(self.item(row,col).whatsThis()).find("#End Repeat Block") == 0:
			#col = col - 1
		if leftBlockIsConditional and not leftShift == 0:
			val = event.pos().x() - (130*leftShift)
			if val<0:
				val = 0
			event = QtGui.QDropEvent(QtCore.QPoint(val,event.pos().y()),event.dropAction(),event.mimeData(),event.mouseButtons(),event.keyboardModifiers(),QtCore.QEvent.Drop)	"""
		if str(self.itemAt(event.pos().x(),event.pos().y()).whatsThis()).find("#End Repeat Block") == 0:
			self.putEndRepeatBlock(row,col)

		super(CustomisedTable, self).dropEvent(event)
		if str(event.source().currentItem().whatsThis()) == testNames[4] and col >= 1:
			tmpItem = QtGui.QTableWidgetItem()
			tmpIcon = QtGui.QIcon("images/repeat_s.png") 
			tmpItem.setIcon(tmpIcon)
			tmpItem.setSizeHint(QtCore.QSize(100,100))
			tmpItem.setWhatsThis("while True:")
			#tmpItem.setFlags(QtCore.Qt.ItemIsEnabled)
			self.setItem(row,col,tmpItem)
			if not self.item(row,self.columnCount()-1) == None:
				self.setColumnCount(self.columnCount()+1)
			self.putEndRepeatBlock(row,col)
		refreshCode(self.parent)

	def putEndRepeatBlock(self,row,col):
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
		tmpItem = QtGui.QTableWidgetItem()
		tmpIcon = QtGui.QIcon("images/repeat_e.png") 
		tmpItem.setIcon(tmpIcon)
		tmpItem.setSizeHint(QtCore.QSize(100,100))
		tmpItem.setWhatsThis("#End Repeat Block")
		#tmpItem.setFlags(QtCore.Qt.ItemIsEnabled)
		self.setItem(row,col+1,tmpItem)

	def returnCode(self):
		code = ""
		for i in range(self.rowCount()):
			if(self.item(i,0)!=None):
				itemText = str(self.item(i,0).whatsThis())
				isCondition = itemText.find("for ")==0 or itemText.find("while ")==0
				if isCondition:
					itemText = self.loopStatement(i,0,2)
				code = code + "	" + itemText + "\n"	
		return self.initCode + code + self.endCode

	def loopStatement(self, row, col, numTabs):
		tab = "\n"
		for i in range(numTabs):
			tab = tab + "\t"
		text = str(self.item(row,col).whatsThis())
		if self.item(row,col+1) == None:
			return text + tab + "break"
		elif str(self.item(row,col+1).whatsThis()).find("#End Repeat Block")==0:
			return text + tab + "break"

		count = 1
		item = self.item(row,col+count)
		while not item == None:
			tmp = str(item.whatsThis())
			if tmp.find("for ") == 0 or tmp.find("while ") == 0:
				tmp = self.loopStatement(row,col+count,numTabs+1)
				while not str(self.item(row,col+count).whatsThis()).find("#End Repeat Block")==0:
					count = count + 1
					if self.item(row,col+count) == None:
						break
			elif tmp.find("#End Repeat Block")==0:
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
		isRepeatBlock = str(self.item(row,col).whatsThis()).find("while ")==0 or str(self.item(row,col).whatsThis()).find("for ")==0
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
		for i in range(4):
			if i == 1:
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
		self.paramList = [["speed","distance(motor encoder value)"]]
		self.setWindowTitle("Block Editor")
		self.text = str(self.item.whatsThis())
		self.index = self.text.find(",")
		if self.text.find("moveForward") == 0:
			self.initForward()
		elif self.text.find("while ") == 0 or self.text.find("for ") == 0 or self.text.find(testNames[4]) == 0:
			self.initRepeat()
		elif self.text.find("if ") == 0 or self.text.find("else ") == 0 or self.text.find("elif ") == 0 or self.text.find(testNames[5]) == 0:
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
		return

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
			if not txt.isdigit():
				reply = QtGui.QMessageBox.information(self, 'Message',"Please type in natural number value", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
				if reply == QtGui.QMessageBox.Ok:
					return
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
