from core.base.model.Module import Module
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler, AnyExcept, Online
from core.base.model.Intent import Intent

import requests
from requests.exceptions import RequestException

class StockTicker(Module):
	"""
	Author: SkyHyperv
	Description: Get variety of stock information

	Dialog:
	- User asks Alice to get some stock information
	- Alice responds: "Can you spell the ticker?"
	- User responds: "M S F T"
	- Alice pulls info and provides to the user

	"""

	def __init__(self):
		super().__init__()
		self._apiKey = self.getConfig('apiKey')

	@IntentHandler('StockTicker')
	@AnyExcept(exceptions=(RequestException, KeyError), text='noServer', printStack=True)
	@Online
	def StockTickerIntent(self, session: DialogSession, **_kwargs):

		if not self._apiKey:
			self.logWarning(msg="Please request an API key from https://www.alphavantage.co/support/#api-key and add it to the module config.json")
			self.endDialog(session.sessionId, text=self.randomTalk('noApiKey'))
			return

		'''url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={self._apiKey}'

		response = requests.get(url=url)
		response.raise_for_status()
		data = response.json()
		self.logInfo(f'DATA: {data}')

		price = data[f'08. previous close']
		

		self.endDialog(session.sessionId, text=self.randomTalk('answer').format(price))
		'''
