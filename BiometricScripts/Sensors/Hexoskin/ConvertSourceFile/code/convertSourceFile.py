import argparse, glob, os, struct, sys, wave
import csv
import ntpath
import itertools as it

VERSION_STRING = "1.2"

"""
(c) Copyright 2015 Hexoskin
Permission to use, copy, modify, and distribute this software for any purpose with or without fee is hereby granted,
provided that the above copyright notice and this permission notice appear in all copies. The software is provided
"as is" and the author disclaims all warranties with regard to this software including all implied warranties of
merchantability and fitness. In no event shall the author be liable for any special, direct, indirect, or
consequential damages or any damages whatsoever resulting from loss of use, data or profits, whether in an action of
contract, negligence or other tortious action, arising out of or in connection with the use or performance of this
software.
"""

"""
ConvertSourceFile.py
    This function demonstrates and implements the decoding of binary data
    as downloaded from the my.hexoskin.com dashboard. Datas are downloaded in
    binary (wav) and CSV format from the dashboard. The code converts them to
    a more "human-friendly" format, then saves it as a CSV in the same
    folder.

    Call python convertSourceFile.py -h for help on options

DEPRECATED: This file is given as an example and to convert file comming from api version 2.4.x. This python script
is not supported anymore. Please use convertSourceFile.c or the the related binary files for conversion.

"""


def main(path, quality_options, group):
    """
    Fetches all .wav files and convert them to CSV
    """
    # First create/set conversion output folder

    output_folder = os.path.join(path, "ConversionOutput/")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if group == 0:
        for file1 in glob.glob(os.path.join(path, '*.wav')):
            try:
                filename = ntpath.basename(file1)
                d = load_wave(file1, quality_options)
                full_file_path = output_folder + filename.replace('wav', 'csv')
                with open(full_file_path, "wb") as f:
                    csv.writer(f).writerows(d)
                print "File %s converted." % (file1)
            except:
                print "File %s problematic or empty, skipped converting." % (file1)

    elif group == 1:
        full_data = {}
        for file1 in glob.glob(os.path.join(path, '*.wav')):
            if 'quality' not in file1 and (('activity' in file1) or ('breathing_rate' in file1) or ('heart_rate' in file1) or
              ('minute_ventilation' in file1) or ('cadence' in file1) or ('tidal_volume' in file1) or 
              ('temperature_celcius' in file1) or ('SPO2' in file1) or ('systolic_pressure' in file1)) :
                d = load_wave(file1, quality_options)
                column_name = (ntpath.basename(file1).split('.')[0])
                full_data[column_name] = zip(*d)

        if quality_options == 'addflags':
            fields = ['timestamp(second)','activity','breathing_rate','breathing_rate_quality','heart_rate','heart_rate_quality',
                      'minute_ventilation','cadence','tidal_volume', 'temperature_celcius', 'SPO2', 'SPO2_quality','systolic_pressure']
            with open(output_folder + "/outputData.csv", "wb") as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                csv.writer(f).writerows(it.izip_longest(full_data['activity'][0],full_data['activity'][1],full_data['breathing_rate'][1],
                    full_data['breathing_rate'][2],full_data['heart_rate'][1],full_data['heart_rate'][2],full_data['minute_ventilation'][1],
                    full_data['cadence'][1], full_data['tidal_volume'][1], full_data['temperature_celcius'][1], full_data['SPO2'][1], full_data['SPO2'][2],
                    full_data['systolic_pressure'][1]))
        elif quality_options == 'remove' or quality_options == 'default':
            fields = ['timestamp(second)','activity','breathing_rate','heart_rate','minute_ventilation','cadence','tidal_volume', 
            'temperature_celcius', 'SPO2', 'systolic_pressure']
            with open(output_folder + "/outputData.csv", "wb") as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                csv.writer(f).writerows(it.izip_longest(full_data['activity'][0],full_data['activity'][1],full_data['breathing_rate'][1],
                    full_data['heart_rate'][1],full_data['minute_ventilation'][1],full_data['cadence'][1],full_data['tidal_volume'][1], 
                    full_data['temperature_celcius'][1], full_data['SPO2'][1], full_data['systolic_pressure'][1]))


def load_async(filename, nsample=None):
    """
    Load an async file (hxd) format. Time t=0 corresponds to the
    beginning of the record.
    """
    yscale = get_scale(filename)
    offset = get_offset(filename)
    y = []
    with open(filename, "rb") as f:
        data = csv.reader(f, delimiter=',')
        for row in data:
            if not row[0].isdigit() and not row[1].isdigit():
                pass
                y.append((float(row[0]), float(row[1])*yscale + offset))
    if nsample:
        y = y[0:nsample]
    return y


def load_wave(filename, csv_format='default', nsample=None):
    """
    Loads a WAV file according to the specified format. Time t=0 corresponds to
    the beginning of the record.
    """
    wav_file = wave.open(filename)

    fs = wav_file._framerate
    y = []
    if fs in [256, 128, 64]:
        offset = 0
    else:
        # This case is for signals with frequency smaller or equal than 1Hz
        offset = 1
        fs = 1. / fs

    for val in range(wav_file._nframes):
        wave_data = wav_file.readframes(1)
        if 'respiration_abdominal' in filename or 'respiration_thoracic' in filename or 'HRV' in filename or 'NN_over_RR' in filename:
            y.append(struct.unpack("<H", wave_data)[0])
        else:
            y.append(struct.unpack("<h", wave_data)[0])

    yscale = get_scale(filename)
    yoffset = get_offset(filename)
    # Format channel according to output options
    filename_quality = filename.replace('.wav', '_quality.wav')
    if csv_format == 'addflags' and os.path.exists(filename_quality):
        y_quality = []
        wav_file_quality = wave.open(filename_quality)
        for val in range(wav_file_quality._nframes):
            wave_data = wav_file_quality.readframes(1)
            y_quality.append(struct.unpack("<h", wave_data)[0])
        d = [((i1 + offset) / float(fs), yy * yscale, yy_quality) for i1, (yy, yy_quality) in enumerate(zip(y, y_quality))]
    elif csv_format == 'remove' and os.path.exists(filename_quality):
        y_quality = []
        wav_file_quality = wave.open(filename_quality)
        for val in range(wav_file_quality._nframes):
            wave_data = wav_file_quality.readframes(1)
            y_quality.append(struct.unpack("<h", wave_data)[0])
        d = [((i1 + offset) / float(fs), yy * yscale + yoffset if not yy_quality else None) for i1, (yy, yy_quality) in enumerate(zip(y, y_quality))]
    else:
        d = [((i1 + offset) / float(fs), yy * yscale + yoffset) for i1, yy in enumerate(y)]
    if nsample:
        d = d[0:nsample]
    return d


def get_scale(filename):
    '''
    Different channels have different amplitude scaling factors.
    The following function explicits those
    '''

    yscale = 1
    filename = os.path.split(filename)[-1]
    if filename in ['activity.wav', 'acceleration_X.wav', 'acceleration_Y.wav', 'acceleration_Z.wav',
                    'RR_interval.csv', 'NN_interval.csv', 'temperature_celcius.csv']:
        yscale = 1/256.
    elif filename in ['minute_ventilation.wav', 'tidal_volume.wav']:
        yscale = 13.28
    elif filename in ['ANN.wav', 'SDNN.wav']:
        yscale = 1/256./16.
    elif filename in ['NN_over_RR.wav', 'HRV_LF_normalized.wav', 'HRV_HF_normalized.wav','HRV_triangular.wav']:
        yscale = 1/100.
    elif filename in ['HRV_HF.wav','HRV_LF.wav']:
        yscale = 1/10.
    elif filename in ['ECG_I.wav','ECG_II.wav', 'ECG_III']:
        yscale = 0.0064
    elif filename in ['minute_ventilation_cl.wav']:
        yscale = 10
    return yscale

def get_offset(filename):
    filename = os.path.split(filename)[-1]

    if filename in ['ECG_I.wav','ECG_II.wav', 'ECG_III.wav']:
        return -1360*get_scale(filename)
    else:
        return 0


if __name__ == "__main__":
    help_text = '''
                This function converts the binary data from the Hexoskin system to CSV format.
                The -q flag specifies how to handle quality data. The -g flag allows creation
                of an outputFile.csv file that contains all the 1Hz data instead of multiple
                independent csv files.
                Example use: python convertSourceFile.py record_37700/ -g 1 -q addflags
                '''
    sign_off = 'Authors: Antoine Gagne <antoine@hexoskin.com>, Simon Dubeau <simondubeau@hexoskin.com>'

    parser = argparse.ArgumentParser(description=help_text, epilog=sign_off)
    parser.add_argument(
        'path',
        # metavar='path',
        action='store',
        type=str,
        nargs=1,
        help='The filepath from which to get the data to convert from')
    parser.add_argument(
        '-q, -quality',
        dest='quality_option',
        # metavar='quality option',
        action='store',
        type=str,
        default='default',
        nargs='?',
        help='Specific output options regarding quality data. Passing "addflags" will append the status flags in the related files. Passing "remove" will remove any value that is deemed unreliable because of quality flags',
        choices=['default', 'remove', 'addflags']
    )
    parser.add_argument(
        '-g, -group',
        dest='group',
        # metavar='group',
        action='store',
        type=int,
        default=0,
        nargs='?',
        help='Set to 1 to group all data together in outputFile.csv instead of outputting it in different files.',
        choices=[0,1]
    )


    args = parser.parse_args()
    main(path=args.path[0],quality_options=args.quality_option,group=args.group)
    
    print "Conversion complete for folder: %s" % args.path
