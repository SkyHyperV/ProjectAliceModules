from __future__ import print_function, unicode_literals
import shutil
from pathlib import Path

try:
	from PyInquirer import style_from_dict, Token, prompt, Validator, ValidationError
except ImportError:
	import subprocess
	import time

	subprocess.run(['pip3', 'install', '-r', 'requirements.txt'])
	time.sleep(1)
	from PyInquirer import style_from_dict, Token, prompt, Validator, ValidationError


STYLE = style_from_dict({
	Token.QuestionMark: '#996633 bold',
	Token.Selected    : '#5F819D bold',
	Token.Instruction : '#99ff33 bold',
	Token.Pointer     : '#673ab7 bold',
	Token.Answer      : '#0066ff bold',
	Token.Question    : '#99ff33 bold',
	Token.Input       : '#99ff33 bold'
})

class NotEmpty(Validator):
	def validate(self, document):
		if not document.text:
			raise ValidationError(
				message='This cannot be empty',
				cursor_position=len(document.text)
			)

PYTHON_CLASS = '''import json

import core.base.Managers as managers
from core.base.model.Intent import Intent
from core.base.model.Module import Module
from core.dialog.model.DialogSession import DialogSession


class {moduleName}(Module):
	"""
	Author: {username}
	Description: {description}
	"""

	def __init__(self):
		self._SUPPORTED_INTENTS	= [
		]

		super().__init__(self._SUPPORTED_INTENTS)


	def onMessage(self, intent: str, session: DialogSession):

		sessionId = session.sessionId
		siteId = session.siteId
		slots = session.slots'''

INSTALL_JSON = '''{{
	"name": "{moduleName}",
	"version": 0.0.1,
	"author": "{username}",
	"maintainers": [],
	"desc": "{description}",
	"aliceMinVersion": 1.0.0,
	"pipRequirements": [{pipRequirements}],
	"systemRequirements": [{systemRequirements}],
	"conditions": {{
		"lang": [{langs}]
	}}
}}'''

DIALOG_TEMPLATE = '''{{
    "module": "{moduleName}",
    "icon": "time",
    "description": "{description}",
    "slotTypes": [
        {{
            "name": "DummySlot",
            "matchingStrictness": null,
            "automaticallyExtensible": false,
            "useSynonyms": true,
            "values": [
                {{
                    "value": "foo",
                    "synonyms": ["bar"]
                }}
            ]
        }}
    ],
    "intents": [
        {{
            "name": "Dummy",
            "description": "REMOVE this dummy intent!",
            "enabledByDefault": true,
            "utterances": [
                "dummy {{foo:=>DummySlotName}}",
                "bar"
            ],
            "slots": [
                {{
                    "name": "DummySlotName",
                    "description": "dummy",
                    "required": false,
                    "type": "DummySlot",
                    "missingQuestion": ""
                }}
            ]
        }}
    ]
}}'''

TALKS = '''{
	"dummy": {
		"default": [
			"foobar",
			"barfoo"
		],
		"short": [
			"foo",
			"bar"
		]
	},
}'''

README = '''# {moduleName}

### Download

##### > WGET method
```bash
wget http://bit.ly/????????? -O ~/ProjectAlice/system/moduleInstallTickets/{moduleName}.install
```

##### > Alice CLI method
```bash
./alice add module {username} {moduleName}
```

### Description
{description}

- Version: 0.0.1
- Author: {username}
- Maintainers: N/A
- Alice minimum version: 1.0.0
- Conditions:
{langs}
- Pip requirements: N/A
- System requirements: N/A

### Configuration


`foo`:
 - type: `bar`
 - desc: `baz`

`bar`:
 - type: `baz`
 - desc: `bar`

'''

WIDGET_CSS = '''.{widgetName} {{
	width: 100%;
	height: 100%;
	background-color: white;
	padding: 5px;
	box-sizing: border-box;
}}
'''

WIDGET_JS = '''$(function(){});'''

WIDGET_TEMPLATE = '''<div class="{widget}" id="{widget}">
	<div class="widgetIcons">
		<div class="widgetIcon">
			<i class="fas fa-calendar-alt"></i>
		</div>
		<div class="widgetIcon" id="widgetSettings_{widget}">
			<i class="fas fa-cog"></i>
		</div>
	</div>
	<div>
		
	</div>
</div>'''

WIDGET_CLASS = '''import sqlite3

from core.base.model.Widget import Widget


class {widget}(Widget):

	SIZE = 'w_small'
	OPTIONS = dict()

	def __init__(self, data: sqlite3.Row):
		super().__init__(data)'''

FIRST_QUESTION = [
	{
		'type'    : 'input',
		'name'    : 'username',
		'message' : 'Please enter your Github user name',
		'validate': NotEmpty,
		'filter'  : lambda val: str(val).capitalize().replace(' ', '')
	},
	{
		'type'    : 'input',
		'name'    : 'moduleName',
		'message' : 'Please enter the name of the module you are creating',
		'validate': NotEmpty,
		'filter'  : lambda val: str(val).title().replace(' ', '')
	}
]

NEXT_QUESTION = [
	{
		'type'    : 'input',
		'name'    : 'description',
		'message' : 'Please enter a description for this module',
		'validate': NotEmpty,
		'filter'  : lambda val: str(val).capitalize()
	},
	{
		'type'    : 'checkbox',
		'name'    : 'langs',
		'message' : 'Choose the language for this module. Note that to share\nyour module on the official repo english is mandatory',
		'validate': NotEmpty,
		'choices' : [
			{
				'name'   : 'en',
				'checked': True
			},
			{
				'name': 'fr'
			},
			{
				'name': 'de'
			},
			{
				'name': 'es'
			},
			{
				'name': 'it'
			},
			{
				'name': 'jp'
			},
			{
				'name': 'kr'
			},
		]
	}
]

def createDestinationFolder(modulePath, answers):
	print('\n----------------------------')
	print('Creating destination folders')

	(modulePath / 'dialogTemplate').mkdir(parents=True)
	(modulePath / 'talks').mkdir(parents=True)

	print('Creating python class')
	Path(modulePath, answers['moduleName']).with_suffix('.py').write_text(
		PYTHON_CLASS.format(
			moduleName=answers['moduleName'],
			description=answers['description'],
			username=answers['username']
		)
	)

def createInstallFile(modulePath, answers):
	reqs = list()
	while True:
		questions = [
			{
				'type'   : 'confirm',
				'name'   : 'requirements',
				'message': 'Do you want to add python pip requirements?',
				'default': False
			},
			{
				'type'    : 'input',
				'name'    : 'req',
				'message' : 'Enter the pip requirement name or `stop` to cancel',
				'validate': NotEmpty,
				'when'    : lambda subAnswers: subAnswers['requirements']
			}
		]
		subAnswers = prompt(questions, style=STYLE)
		if not subAnswers['requirements'] or subAnswers['req'] == 'stop':
			break
		reqs.append(subAnswers['req'])

	sysreqs = list()
	while True:
		questions = [
			{
				'type'   : 'confirm',
				'name'   : 'sysrequirements',
				'message': 'Do you want to add system requirements?',
				'default': False
			},
			{
				'type'    : 'input',
				'name'    : 'sysreq',
				'message' : 'Enter the requirement name or `stop` to cancel',
				'validate': NotEmpty,
				'when'    : lambda subAnswers: subAnswers['sysrequirements']
			}
		]
		subAnswers = prompt(questions, style=STYLE)
		if not subAnswers['sysrequirements'] or subAnswers['sysreq'] == 'stop':
			break
		sysreqs.append(subAnswers['sysreq'])

	print('Creating install file')
	langs = ','.join([f'\n\t\t\t"{lang}"' for lang in answers['langs']])
	if langs:
		langs += '\n\t\t'

	pipRequirements = ','.join([f'\n\t\t"{req}"' for req in reqs])
	if pipRequirements:
		pipRequirements += '\n\t'

	systemRequirements = ','.join([f'\n\t\t"{req}"' for req in sysreqs])
	if systemRequirements:
		systemRequirements += '\n\t'

	Path(modulePath, answers['moduleName']).with_suffix('.install').write_text(
		INSTALL_JSON.format(
			moduleName=answers['moduleName'],
			description=answers['description'],
			username=answers['username'],
			langs=langs,
			pipRequirements=pipRequirements,
			systemRequirements=systemRequirements
		)
	)

def createDialogTemplates(modulePath, answers):
	print('Creating dialog template(s)')
	for lang in answers['langs']:
		print(f'- {lang}')
		Path(modulePath, 'dialogTemplate', lang).with_suffix('.json').write_text(
			DIALOG_TEMPLATE.format(
				moduleName=answers['moduleName'],
				description=answers['description'],
				username=answers['username']
			)
		)

def createTalks(modulePath, answers):
	print('Creating talks')
	for lang in answers['langs']:
		print(f'- {lang}')
		Path(modulePath, 'talks', lang).with_suffix('.json').write_text(TALKS)

def createReadme(modulePath, answers):
	print('Creating readme file')
	langs = ''
	for lang in answers['langs']:
		langs += f'  - {lang}\n'

	Path(modulePath, 'README.md').write_text(
		README.format(
			moduleName=answers['moduleName'],
			description=answers['description'],
			username=answers['username'],
			langs=langs.rstrip()
		)
	)

def createWidgets(modulePath, answers):
	moduleWidgets = []
	while True:
		questions = [
			{
				'type'   : 'confirm',
				'name'   : 'widgets',
				'message': 'Are you planning on creating widgets for you module? Widgets are used on the\ninterface to display quick informations that your module can return' if not moduleWidgets else 'Any other widgets?',
				'default': False
			},
			{
				'type'    : 'input',
				'name'    : 'widget',
				'message' : 'Enter the name of the widget',
				'validate': NotEmpty,
				'when'    : lambda subAnswers: subAnswers['widgets']
			}
		]
		subAnswers = prompt(questions, style=STYLE)
		if not subAnswers['widgets'] or subAnswers['widget'] == 'stop':
			break
		moduleWidgets.append(subAnswers['widget'])

	if not moduleWidgets:
		return
	
	print('Creating widgets base directories')
	(modulePath / 'widgets' / 'css').mkdir(parents=True, exist_ok=True)
	(modulePath / 'widgets' / 'fonts').mkdir(parents=True, exist_ok=True)
	(modulePath / 'widgets' / 'img').mkdir(parents=True, exist_ok=True)
	(modulePath / 'widgets' / 'js').mkdir(parents=True, exist_ok=True)
	(modulePath / 'widgets' / 'lang').mkdir(parents=True, exist_ok=True)
	(modulePath / 'widgets' / 'templates').mkdir(parents=True, exist_ok=True)

	(modulePath / 'widgets' / '__init__.py').touch(exist_ok=True)
	(modulePath / 'widgets' / 'css' / 'common.css').touch(exist_ok=True)
	(modulePath / 'widgets' / 'img' / '.gitkeep').touch(exist_ok=True)
	(modulePath / 'widgets' / 'fonts' / '.gitkeep').touch(exist_ok=True)

	for widget in moduleWidgets:
		widget = str(widget).title().replace(' ', '')
		(modulePath / 'widgets' / 'css' / f'{widget}.css').write_text(WIDGET_CSS.format(widgetName=widget))
		(modulePath / 'widgets' / 'js' / f'{widget}.js').write_text(WIDGET_JS)
		(modulePath / 'widgets' / 'lang' / f'{widget}.lang.json').write_text('{}')
		(modulePath / 'widgets' / 'templates' / f'{widget}.html').write_text(WIDGET_TEMPLATE.format(widget=widget))
		(modulePath / 'widgets' / f'{widget}.py').write_text(WIDGET_CLASS.format(widget=widget))


def cli():
	print('\nHey welcome in this basic module creation tool!')
	answers = prompt(FIRST_QUESTION, style=STYLE)

	modulePath = Path.home() / 'ProjectAliceModuler' / answers['username'] / answers['moduleName']

	while modulePath.exists():
		questions = [
			{
				'type'   : 'confirm',
				'name'   : 'delete',
				'message': 'Seems like this module name already exists.\nDo you want to delete it locally?',
				'default': False
			},
			{
				'type'    : 'input',
				'name'    : 'moduleName',
				'message' : 'Ok, so chose another module name please',
				'validate': NotEmpty,
				'filter'  : lambda val: str(val).title().replace(' ', ''),
				'when'    : lambda subAnswers: not subAnswers['delete']
			}
		]
		subAnswers = prompt(questions, style=STYLE)
		if subAnswers['delete']:
			shutil.rmtree(path=modulePath)
		else:
			modulePath = Path.home() / 'ProjectAliceModuler' / answers['username'] / subAnswers['moduleName']
			answers['moduleName'] = subAnswers['moduleName']

	subAnswers = prompt(NEXT_QUESTION, style=STYLE)
	answers = {**answers, **subAnswers}

	createDestinationFolder(modulePath, answers)
	createInstallFile(modulePath, answers)
	createDialogTemplates(modulePath, answers)
	createTalks(modulePath, answers)
	createReadme(modulePath, answers)
	createWidgets(modulePath, answers)

	print('----------------------------\n')
	print('All done!')
	print('You can now start creating your module. You will find the main class in {}/{}.py'.format(modulePath, answers['moduleName']))
	print('\nRemember to edit the dialogTemplate/XYZ.json and remove the dummy data!!\n')
	print('Thank you for creating for Project Alice')


if __name__ == '__main__':
	cli()
