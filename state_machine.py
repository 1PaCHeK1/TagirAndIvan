import abc

class State(abc.ABC):
	machine : object
	prev : object

	def __init__(self, prev, machine):
		self.prev = prev
		self.machine = machine
	
	@abc.abstractmethod
	def active(self, **kwargs):
		pass

	@abc.abstractmethod	
	def movenext(self):
		pass

	def moveprev(self):
		return self.prev

class State1(State):
	def active(self, **kwargs):
		print("Пустой барабан для монетки", self.machine.n, "рубля")
	
def movenext(self):
		if self.machine.n >= 5:
			return State3(None, self.machine)
		else:
			return State2(None, self.machine)
	
class State2(State):
	def active(self, **kwargs):
		print("Монетка выпала", self.machine.n)
	
	def movenext(self):
		return State7(self, self.machine)	

class State3(State):

	def active(self, **kwargs):
		print("В барабане есть монетка")
	
	def movenext(self):
		self.machine.n -= 5
		return State4(self, self.machine)
		
class State4(State):
	def active(self, **kwargs):
		print("Барабан прокрутили")
	
	def movenext(self):
		return State5(self, self.machine)

class State5(State):
	def active(self, **kwargs):
		print("Выдать шарик")
	
	def movenext(self):
		if self.machine.n < 5:
			return State6(None, self.machine)
		else:
			return State1(None, self.machine)

class State6(State):
	def active(self, **kwargs):
		print("Деньги закончились")
	
	def movenext(self):
		return State7(self, self.machine)
	
class State7(State):
	def active(self, **kwargs):
		print("Возврат барабана в исходное состояние")
	
	def movenext(self):
		raise StopIteration()

class Machine(State):
	n : int
	current : State

	def __init__(self, n):
		self.n = n
		self.current = State1(None, self)

	def active(self, **kwargs):
		self.current.active(**kwargs)

	def movenext(self):
		self.current = self.current.movenext()

s = Machine(5)
for _ in range(14):
	s.active()
	s.movenext()
#чыты дла гзг0
# open > 0.zip