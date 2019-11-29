from core.base.model.Module import Module
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler, AnyExcept, Online
from core.base.model.Intent import Intent

import requests
from requests.exceptions import RequestException

'''
TODO:
- output price in user's native/base currency
'''

class StockTicker(Module):
	"""
	Author: SkyHyperV
	Description: Get stock price
	"""

	def __init__(self):
		super().__init__()
		self._apiKey = self.getConfig('apiKey')


	@staticmethod
	def _extractTicker(session: DialogSession) -> str:
		if 'Letters' in session.slots:
			return ''.join([slot.value['value'] for slot in session.slotsAsObjects['Letters']])
		return


	def _searchTicker(self, session: DialogSession, question: str):
		ticker = self._extractTicker(session)

		if not ticker:
			self.continueDialog(
				sessionId=session.sessionId,
				text=self.randomTalk(text=question),
				intentFilter=[Intent('SpellWord')],
				currentDialogState='searchTicker'
			)

		return ticker


	@IntentHandler('StockTicker')
	@IntentHandler('SpellWord', isProtected=True, requiredState='searchTicker')
	@AnyExcept(exceptions=(RequestException, KeyError), text='noServer', printStack=True)
	@Online
	def StockTickerIntent(self, session: DialogSession, **_kwargs):

		if not self._apiKey:
			self.logWarning(msg="Please request an API key from https://www.alphavantage.co/support/#api-key and add it to the module config.json")
			self.endDialog(session.sessionId, text=self.randomTalk('noApiKey'))
			return

		ticker = self._searchTicker(session, 'searchTicker')

		if not ticker:
			self.endDialog(session.sessionId, text=self.randomTalk('noMatch'))
		else:

			# get the name of the company first to make a better experience for the user
			url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={ticker}&apikey={self._apiKey}'
			response = requests.get(url=url)
			response.raise_for_status()
			data = response.json()
			name = data[f'bestMatches'][0][f'2. name']

			# get the stock price
			url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={self._apiKey}'
			response = requests.get(url=url)
			response.raise_for_status()
			data = response.json()
			price = float(data[f'Global Quote'][f'08. previous close'])
			price = str(f'{price:4.2f}')
			dollars = int(price.split('.')[0])
			cents = int(price.split('.')[1])

			self.endDialog(session.sessionId, text=self.randomTalk('answer').format(name,dollars,cents))
