from core.base.model.Module import Module
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler


class HomeAssistant(Module):
	"""
	Author: SkyHyperv
	Description: Home Assistant integration
	"""

	@IntentHandler('AlarmOn')
	def haIntentEater(self, session: DialogSession, **_kwargs):
		self.endSession(session.sessionId)


	@IntentHandler('AlarmOff')
	def haIntentEater(self, session: DialogSession, **_kwargs):
		self.endSession(session.sessionId)

	@IntentHandler('OutdoorClimate')
	def haIntentEater(self, session: DialogSession, **_kwargs):
		self.endSession(session.sessionId)

	@IntentHandler('HomeClimate')
	def haIntentEater(self, session: DialogSession, **_kwargs):
		self.endSession(session.sessionId)

	@IntentHandler('WeatherSummary')
	def haIntentEater(self, session: DialogSession, **_kwargs):
		self.endSession(session.sessionId)

	@IntentHandler('ClimateClosestStorm')
	def haIntentEater(self, session: DialogSession, **_kwargs):
		self.endSession(session.sessionId)
