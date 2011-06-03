# English Helper for Chinese
# v0.08 - 11th April 2010
# Harry Eakins - harry.eakins at googlemail dot com
#
# This plugin adds an English model and auto-generates English and Chinese definitions for the inputted word.


import sys, os, re
from ankiqt import mw

ankidir = mw.config.configPath
plugdir = os.path.join(ankidir, "plugins")
plugdir = os.path.join(plugdir, "englishhelper_zh-tw")
sys.path.insert(0, plugdir)

from anki.hooks import addHook
from anki.db import *
from pystardict import Dictionary
import english_model
from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

##### Dictionary functions ######

ecDict = None
def findMandarinDef(word):
    if word == '':
        return ''
    global ecDict
    if ecDict is None:
        ecDict = Dictionary(os.path.join(os.path.dirname(os.path.realpath( __file__ )), 'englishhelper_zh-tw', u'stardict-xdict-ec-big5-2.4.2', u'xdict-ec-big5'))
    
    try:
        definition = ecDict[word]
        ecregex = re.compile("(.*?)\\x00...([\s\S]*)")        
        return ecregex.search(unicode(definition, 'utf-8')).group(2).replace(u'\n', u'<br />')
    except KeyError:
        return ''

eeDict = None
def findEnglishDef(word):
    if word == '':
        return ''
    global eeDict
    if eeDict is None:
        eeDict = Dictionary(os.path.join(os.path.dirname(os.path.realpath( __file__ )), 'englishhelper_zh-tw', u'stardict-mwc-2.4.2', u'mwc'))
    definitionList = []
    try:
    # Grab the dictionary entry
        dictPage = eeDict[word]

    # Create regular expression which will match definitions
        eeregex = re.compile("<dtrn>\s*([\s\S]*?)\s*</dtrn>")

    # Retrieve all matches of the regular expression
        definitions = eeregex.findall(dictPage)

    # Create definition list and initialize to empty
        definitionList = u''
        i = 1
        
    # Build definition list
        for line in definitions:
            definitionList += u'(' + unicode(str(i), 'utf-8') + u') ' + unicode(line, 'utf-8') + u'<br />'
            i += 1

    except KeyError:
        return ''

    return definitionList


from audioGetter import getAudio
from anki.deck import Deck

audioSetting = True

def fetchAudioToggle():
    global audioSetting
    global menu1
    audioSetting = not audioSetting
    if audioSetting == True:
        menu1.setText("Don't Fetch English Pronunciation Audio")
    else:
        menu1.setText("Fetch English Pronunciation Audio")

def findEnglishPro(word):
    if word == '':
        return ''
    global ecDict
    if ecDict is None:
        ecDict = Dictionary(os.path.join(os.path.dirname(os.path.realpath( __file__ )), 'englishhelper_zh-tw', 'stardict-xdict-ec-big5-2.4.2', 'xdict-ec-big5'))
    
    try:
        fieldvalue = ''
        # skip Get pronunciation in IPA
        '''
        try:
            definition = ecDict[word]
            regex = re.compile("(.*?)\\x00...([\s\S]*)")        
            IPA =  regex.search(unicode(definition, 'utf-8')).group(1)
            unicodeFontList = "'DejaVu Sans, Arial Unicode MS, Charis SIL'"
            fieldvalue += u"<font face=" + unicodeFontList + u">" + IPA + u'</font>'
        except:
            pass
        '''
        if audioSetting == True:
            # Get pronunciation in audio
            try:
                audio = getAudio(word)
                audioFilename = word + ".wav"
                folder = os.path.join(mw.deck.mediaDir(create=True),word[0])
                if not os.path.exists(folder):
                    os.mkdir(folder)
                audioFile = open(os.path.join(folder, audioFilename), "w")
                audioFile.write(audio.read());
                audioFile.close()
                fieldvalue += u"[sound:" + audioFilename[0]+u'/'+audioFilename + u"]"
            except:
                pass
            
        # Return pronunciation
        return fieldvalue
    except KeyError:
        return ''


##### Handler functions #######

def onFocusLost(fact, field):
    if field.name != 'English Word':
        return

    searchword = field.value.lower().strip()    
    try:
        if fact['Chinese Definition'] == "": # Generate if empty
                fact['Chinese Definition'] = findMandarinDef(searchword)
    except KeyError:
        pass

    try:
        if fact['English Definition'] == "": 
                fact['English Definition'] = findEnglishDef(searchword)
    except KeyError:
        pass

    try:
        if fact['English Pronunciation'] == "":
                fact['English Pronunciation'] = findEnglishPro(searchword)
    except KeyError:
        pass

addHook('fact.focusLost', onFocusLost)

# Setup menu entries
menu1 = QAction(mw)
menu1.setText("Don't Fetch English Pronunciation Audio")
mw.connect(menu1, SIGNAL("triggered()"),fetchAudioToggle)

mw.mainWin.menuTools.addSeparator()
mw.mainWin.menuTools.addAction(menu1)
mw.registerPlugin("English Helper for Chinese zh-tw", 0.10) 
