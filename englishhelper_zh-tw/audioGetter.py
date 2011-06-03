import urllib, re

# Returns a pronunciation wav file from Merriam-Webster.com
# If no audio found, returns None
def getAudio(word):
    try:
        # Download the dictionary webpage
        webpage = urllib.urlopen("http://www.merriam-webster.com/dictionary/" + word)
        # webpage = open(word + ".html")

        # Convert to html string
        html = webpage.read()

        # Find the wav file identifiers
        reg = re.compile("headword.*?return au\('([^']*)'[^']*'([^']*)'\);")
        ids = reg.findall(html)[0]
    except Exception:
        return None    # Could not get audio file for some reason

    try:

        # Download audio play webpage
        audioWebPage = urllib.urlopen("http://www.merriam-webster.com/cgi-bin/audio.pl?" + ids[0] + "=" + ids[1])
        # audioWebPage = open("audio.pl " + ids[0] + "=" + ids[1] + ".html")
        audioHtml = audioWebPage.read()

        # Find the URL for the wav file
        reg = re.compile('<A HREF="(http[^"]*)"')
        audioURL = reg.findall(audioHtml)[0]

        # Download the audio
        audioFile = urllib.urlopen(audioURL)
    except Exception:
        return None    # Could not get audio file for some reason

    return audioFile

