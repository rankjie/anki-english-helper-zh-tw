from anki.hooks import addHook
from anki.db import *
from anki.models import Model, CardModel, FieldModel
import anki.stdmodels

# Create a defualt model called "English" for use with the English Helper plugin
def EnglishModel():
    m = Model(_("English"))

    tempFieldModel = FieldModel(u'English Word', False, False)
    tempFieldModel.editFontSize = 14
    m.addFieldModel(tempFieldModel)
    tempFieldModel = FieldModel(u'Chinese Definition', False, False)
    tempFieldModel.editFontSize = 16
    m.addFieldModel(tempFieldModel)
    tempFieldModel = FieldModel(u'English Definition', False, False)
    tempFieldModel.editFontSize = 14
    m.addFieldModel(tempFieldModel)
    tempFieldModel = FieldModel(u'English Pronunciation', False, False)
    tempFieldModel.editFontSize = 14
    m.addFieldModel(tempFieldModel)
    tempFieldModel = FieldModel(u'Example Sentence', False, False)
    tempFieldModel.editFontSize = 14
    m.addFieldModel(tempFieldModel)
    m.addCardModel(CardModel(u"Recognition",
                             u"%(English Word)s",
                             u"%(Chinese Definition)s<br />%(English Definition)s<br />%(English Pronunciation)s \
                                <br /><font color='red'>%(Example Sentence)s</font>"))
    m.tags = u"English"
    return m

anki.stdmodels.models['English'] = EnglishModel


###### Resize fields #####
# Because the definition field should be bigger than the word field etc

def resize(widget, field):
    if field.name == "English Word":
        widget.setFixedHeight(35)
    elif field.name == "Chinese Definition":
        widget.setFixedHeight(50)
    elif field.name == "English Definition":
        widget.setMaximumHeight(500)
    elif field.name == "Example Sentence":
        widget.setFixedHeight(100)
    elif field.name == "English Pronunciation":
        widget.setFixedHeight(30)

addHook("makeField", resize) 


