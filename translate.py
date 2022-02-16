"""This script shows how to use the isdetranslator module from the command
line."""
import isdetranslator
import sys
import urllib.request

if __name__ == '__main__':

    __output_type = None
    __help = False
    __mode = False
    __input = None
    __raw = None

    helptext = """
    Usage:

        translate <input_file> -d|-s [-o <output_file>]
        translate -h

        Flags:
            -d    Convert to W3C Data Catalogue Vocabulary
            -h    Display this help page
            -s    Convert to Schema.org
    
    """

    #
    # Process the arguments passed to the script
    #
    for i, arg in enumerate(sys.argv):

        if i > 1 and arg.lower() == '-s':
            __output_type = isdetranslator.SerialiseAs.SCHEMAORG
        elif i > 1 and arg.lower() == '-d':
            __output_type = isdetranslator.SerialiseAs.DCAT
        elif arg.lower == '-h':
            __help = True
        elif i==1 and arg.startswith('http://') or arg.startswith('https://') or arg.startswith('ftp://'):
            __input = arg
            __mode = isdetranslator.DataMode.WEB
        elif i==1:
            __input = arg
            __mode = isdetranslator.DataMode.FILE

    #
    # Validate the invocation
    #
    if not __output_type:
        raise isdetranslator.NoOrIncorrectOutputFormatSupplied

    if not __input:
        raise isdetranslator.NoInputDataSourceSupplied

    if not __help:
        #
        # Parse the input
        #
        if __mode == isdetranslator.DataMode.WEB:
            with urllib.request.urlopen(__input) as u:
                __raw = u.read()
        elif __mode == isdetranslator.DataMode.FILE:
            pass

        if __raw:
            isdeobj = isdetranslator.Dataset()
            if __mode == isdetranslator.DataMode.WEB:
                isdeobj.set(isdetranslator.DatasetProperties.SOURCE, __input)
            isdeobj.fromXML(__raw)
            print(isdeobj.abstract())
        
    else:
        #
        # Print the help text
        #
        print(helptext)
