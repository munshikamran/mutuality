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
	def __init__(self,Profile):
		self.profile = Profile
		self.spinBothSlots()

	def printState(self):
		print self.leftSlot['name'] + ' and ' + self.rightSlot['name']

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
