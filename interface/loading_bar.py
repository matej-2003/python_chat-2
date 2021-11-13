import time
import datetime

class LoadingBar:
	def __init__(self, l, fg="#", bg=".", bar_l=10):
		self.l = l
		self.bar_l = bar_l
		self.fg = fg
		self.bg = bg
		self.screen = ""
		self.step = 0

	def progress(self):
		self.screen = ""
		buffer = self.fg * (self.l - self.step)
		if self.step + self.bar_l > self.l:
			off = self.step + self.bar_l - self.l
			self.screen = self.bg * (off) + self.fg * (self.step - off) + self.bg * self.bar_l + buffer
		else:
			self.screen = self.fg * self.step + self.bg * self.bar_l + buffer
		self.screen = self.screen[0:self.l]
		self.step = (self.step+1) % self.l

	def get(self):
		self.progress()
		return self.screen

	@staticmethod
	#simple spinner animation n is the iterator
	def spinner(n):
		spin_char = "|/-\\"
		return spin_char[n % len(spin_char)]

	@staticmethod
	def waiting_animation(p, display, text="Connecting", form="[{b}{s}] {t}"):
		start = time.time()
		bar = LoadingBar(30, bar_l=10, fg=" ", bg=".")

		while p.is_alive():
			screen = text + form.format(
				b=bar.get(),
				s=LoadingBar.spinner(bar.step),
				t=datetime.timedelta(seconds=(time.time() - start))
			)
			display(screen)
			time.sleep(0.1)