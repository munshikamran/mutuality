from connect.models import Profile

#example usage
# from connect.models import Profile
# from slotMachine import SlotMachine
# x = Profile.objects.all()[0]
# slotMachine = SlotMachine(x)
# slotMachine.spinBothSlots()
# slotMachine.printState()

class SlotMachine:
	profile = None
	leftSlot = None
	rightSlot = None
	leftSlotLocked = False
	rightSlotLocked = False
	def __init__(self,Profile):
		self.profile = Profile
		self.spinBothSlots()

	#public methods
	def spinButtonPressed(self):
		if self.leftSlotLocked and not self.rightSlotLocked:
			self.spinRightSlot()
		elif self.rightSlotLocked and not self.leftSlotLocked:
			self.spinLeftSlot()
		elif self.rightSlotLocked and self.leftSlotLocked:
			self.spinBothSlots()

	def leftLockButtonPressed(self):
		self.leftSlotLocked = not self.leftSlotLocked

	def rightLockButtonPressed(self):
		self.rightSlotLocked = not self.rightSlotLocked

	def printState(self):
		print self.leftSlot['name'] + ' and ' + self.rightSlot['name']

	#private
	def spinLeftSlot(self):
		if self.rightSlot == None:
			self.leftSlot = self.profile.getRandomFriend()
		else:
			potentials = self.profile.getFriendOptimumPotentials(self.rightSlot)
			match = self.profile.getMatchForFriendFromPotentials(self.rightSlot,potentials)
			self.leftSlot = match[1]

	def spinRightSlot(self):
		if self.leftSlot == None:
			self.profile.getRandomFriend()
		else:
			potentials = self.profile.getFriendOptimumPotentials(self.leftSlot)
			match = self.profile.getMatchForFriendFromPotentials(self.leftSlot,potentials)
			self.rightSlot = match[1]

	def spinBothSlots(self):
		self.leftSlot = None
		self.rightSlot = None
		self.spinLeftSlot()
		self.spinRightSlot()