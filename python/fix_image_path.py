# -*- coding: utf-8 -*-
#!/usr/bin/python
#
# Script to update fields related to path images in a CSV file
# where Magento Bulk Importer looks for images.
#
# @author: Moises Brenes

import os
import sys
import getopt
import csv

def main(argv):
    export_file = str()
    output_file = 'output.csv'

    try:
        opts, args = getopt.getopt(argv, 'hi:', ['help', 'export_file='])
    except getopt.GetoptError:
        usage(2)
    for opt, arg in opts:
        if opt == '-h':
            usage(0)
        elif opt in ('-i', '--export_file'):
            export_file = arg

    if os.path.exists(export_file):
        fix_path(export_file, output_file)
    else:
        usage(2)

def usage(errno):
    print 'fix_image_path.py -i <export_file>'
    sys.exit(errno)

def fix_path(export_file, output_file):
    export = open(export_file, 'rb')
    reader = csv.reader(export, delimiter=',', quotechar='"')

    output = open(output_file, 'wb')
    writer = csv.writer(output, delimiter=',', quotechar='"')

    fields = (
        'image',
        'small_image',
        'thumbnail',
        'gallery',
    )
    position = list()

    rownum = 0
    for row in reader:
        if rownum == 0:
            colnum = 0
            for col in row:
                if col in fields:
                    position.append(colnum)
                colnum += 1

            writer.writerow(row)
        else:
            colnum = 0
            update = list()
            for col in row:
                if colnum in position and len(col) > 0:
                    field = col.split(',')
                    path = str()
                    for s in field:
                        if len(s) > 0:
                            path += '%s,' % s[s.rfind('/'):]
                    col = path
                colnum += 1

                update.append(col)
            writer.writerow(update)

        rownum += 1

    export.close()
    output.close()

if __name__ == '__main__':
    main(sys.argv[1:])
