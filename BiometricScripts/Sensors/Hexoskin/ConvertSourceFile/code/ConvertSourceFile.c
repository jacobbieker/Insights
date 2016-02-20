
/*
 ConvertSourceFile.c
 
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
 ConvertSourceFile.c
 This function demonstrates and implements the decoding of binary data
 as downloaded from the my.hexoskin.com dashboard. Datas are downloaded in
 binary (wav) format from the dashboard. The code converts them to
 a more "human-friendly" format, then saves it as a CSV in the same
 folder.
 
 
 gcc ConvertSourceFile.c -o mac/ConvertSourceFile
 gcc ConvertSourceFile.c -o ubuntu/ConvertSourceFile
 gcc ConvertSourceFile.c -o windows/ConvertSourceFile
 
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>  /* abs */
#include <sys/stat.h>
#include "tinydir.h"


const int  ADD_QUALITY = 1;
const int   GROUPED = 2;
const int   HEADER = 4;
const int   EPOCH = 8;

const int  one_hz[] = {11, 12, 13, 14, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26};
const int MAJOR = 0;
const int MINOR = 4;
const int MICRO = 0;

const double wav_ref_table[][7] = { //dt,dt_offset, gain, offset, signed, round, datatype
  {1./256., 0, 0.0064, -1360*0.0064, 1, 5, 4113}, //ECG_I, 0
  {1./256., 0, 0.0064, -1360*0.0064, 1, 5, 4114}, //ECG_II,
  {1./256., 0, 0.0064, 0, 1, 5, 4115}, //ECG_III,
  {2./256, 0, 1, 0, 0, 5, 4129}, //respiration_thoracic,
  {2./256, 0, 1, 0, 0, 5, 4130}, //respiration_abdominal,
  {4./256, 0, 1/256., 0, 1, 8, 4145}, //acceleration_X, 5
  {4./256, 0, 1/256., 0, 1, 8, 4146}, //acceleration_Y,
  {4./256, 0, 1/256., 0, 1, 8, 4147}, //acceleration_Z,
  {4./256, 0, 1, 0, 0, 5, 64}, //ppgdo,
  {4./256, 0, 1, 0, 0, 0, 64}, //ppgDisc, DEPRECATED
  {4./256, 0, 1, 0, 0, 5, 64}, //ppgOOT, 10 DEPRECATED
  {1., 1, 1, 0, 0, 0, 19}, //heart_rate,
  {1., 1, 1, 0, 0, 0, 1000}, //heart_rate_quality,
  {1., 1, 1, 0, 0, 0, 33}, //breathing_rate,
  {1., 1, 1, 0, 0, 0, 1001}, //breathing_rate_quality,
  {1., 1, 13.28, 0, 0, 5, 36}, //minute_ventilation, 15
  {1., 1, 13.28, 0, 0, 5, 37}, //tidal_volume,
  {1., 1, 10, 0, 0, 5, 36}, //minuteventilation_cl,
  {1., 1, 1, 0, 0, 5, 37}, //tidal_volume_ml,
  {1., 1, 1/256., 0, 1, 8, 49}, //activity,
  {1., 1, 1, 0, 0, 0, 53}, //cadence,   20
  {1., 1, 1/256., 0, 1, 8, 81}, //temperature_celcius,
  {1., 1, 1, 0, 0, 5, 98}, //systolic_pressure
  {1., 1, 1, 0, 0, 0, 66}, //SPO2,
  {1., 1, 1, 0, 0, 0, 1002}, //SPO2_quality,  25
  {1., 1, 1, 0, 0, 0, 247}, //BATT_ST_CHANNEL_CHAR,
  {1., 1, 1, 0, 0, 0, 246}, //TEMP_ST_CHANNEL_CHAR,
  {300., 300, 1./10., 0, 0, 8, 277}, //HRV_HF,
  {300., 300, 1./100, 0, 0, 8, 273}, //HRV_LF_normalized,
  {300., 300, 1./10, 0, 0, 8, 276}, //HRV_LF,
  {300., 300, 1./100, 0, 0, 8, 274}, //NN_over_RR, //30
  {300., 300, 1./256./16., 0, 0, 8, 271}, //ANN,
  {300., 300, 1./256./16., 0, 0, 8, 272}, //SDNN,
  {300., 300, 1./100., 0, 0, 5, 275}, //HRV_triangular,
  {4./256, 0, 1, 0, 0, 5, 64}, //PPG,
};


const char *wav_name[][4] = {
  //wave_name, csv_name, quality_signal_name, unit
  {"ECG_I", "ECG_I", "", "mV"}, //0
  {"ECG_II", "ECG_II", "", "mV"},
  {"ECG_III", "ECG_III", "", "mV"},
  {"respiration_thoracic", "respiration_thoracic", "", "na"},
  {"respiration_abdominal", "respiration_abdominal", "", "na"},
  {"acceleration_X", "acceleration_X", "", "G"}, //5
  {"acceleration_Y", "acceleration_Y", "", "G"},
  {"acceleration_Z", "acceleration_Z", "", "G"},
  {"ppgdo", "ppgdo", "", "na"},
  {"ppgDisc", "ppgDisc", "", "na"},
  {"ppgOOT", "ppgOOT", "", "na"}, //10
  {"heart_rate", "heart_rate", "heart_rate_quality", "bpm"},
  {"heart_rate_quality", "heart_rate_quality", "NONE", "na"},
  {"breathing_rate", "breathing_rate", "breathing_rate_quality", "rpm"},
  {"breathing_rate_quality", "breathing_rate_quality", "NONE", "na"},
  {"minute_ventilation", "minute_ventilation", "", "ml/min"}, // DEPRECATED 15
  {"tidal_volume", "tidal_volume", "", "ml"}, //DEPRECATED
  {"minute_ventilation_cl", "minute_ventilation", "", "ml/min"}, //same destination as minute_ventilation, if both are present overwrite the first
  {"tidal_volume_ml", "tidal_volume", "", "ml"}, //same destination as minute_ventilation, if both are present overwrite the first
  {"activity", "activity", "", "G"},
  {"cadence", "cadence", "", "spm"}, //20
  {"temperature_celcius", "temperature_celcius", "", "Celcius"},
  {"systolic_pressure", "systolic_pressure", "", "mmHg"},
  {"SPO2", "SPO2", "SPO2_quality", "Percent"},
  {"SPO2_quality", "SPO2_quality", "NONE", "na"},
  {"BATT_ST_CHANNEL_CHAR", "BATT_ST_CHANNEL_CHAR", "", "na"},//25
  {"TEMP_ST_CHANNEL_CHAR", "TEMP_ST_CHANNEL_CHAR", "", "na"},
  {"HRV_HF", "HRV_HF", "", "ms^2"},
  {"HRV_LF_normalized", "HRV_LF_normalized", "", ""},
  {"HRV_LF", "HRV_LF", "", "ms^2"},
  {"NN_over_RR", "NN_over_RR", "", "na"}, //30
  {"ANN", "ANN", "", "s"},
  {"SDNN", "SDNN", "", "s"},
  {"HRV_triangular", "HRV_triangular", "", "na"},
  {"PPG", "PPG", "", "na"},
};

const char *csv_name[][4] = {
  //csv_name, csv_epoch_name, none, unit
  {"QRS", "QRS_epoch", "", "na"},
  {"RR_interval", "RR_interval_epoch", "", "s"},
  {"inspiration", "inspiration_epoch", "", "na"},
  {"expiration", "expiration_epoch", "", ""},
  {"step", "step_epoch", "", "step"},
  {"PTT", "PTT_epoch", "", "s"},
  {"device_position", "device_position_epoch", "", "na"},
  {"sleep_position", "sleep_position_epoch", "", "na"},
  {"sleep_phase", "sleep_phase_epoch", "", "ma"},
  {"NN_interval", "NN_interval_epoch", "", "s"},
  {"RR_interval_realigned", "RR_interval_realigned_epoch", "", "s"},
  {"RR_interval_quality", "RR_interval_quality_epoch", "", "na"},
};

const double csv_ref_table[][7] = {  //dt, dt_offset, gain, offset, signed, round, datatype
  {1., 0, 1., 0, 0, 0, 17}, //QRS
  {1., 0, 1/256., 0, 0, 8, 18}, //RR_interval
  {1., 0, 1., 0, 0, 0, 34}, //inspiration
  {1., 0, 1., 0, 0, 0, 35}, //expiration
  {1., 0, 1., 0, 0, 0, 52}, //step
  {1., 0, 1./256, 0, 0, 0, 97}, //PTT
  {1., 0, 1., 0, 0, 0, 269}, //device_position
  {1., 0, 1., 0, 0, 0, 270}, //sleep_position
  {1., 0, 1., 0, 0, 0, 280}, //sleep_phase
  {1., 0, 1/256., 0, 0, 8, 318}, //NN_interval
  {1., 0, 1/256., 0, 0, 8, 319}, //RR_interval_realigned
  {1., 0, 1., 0, 0, 0, 1004}, //RR_interval_quality
};

const int n_one_hz = sizeof(one_hz) / sizeof(one_hz[0]);
const int n_wav_chan = sizeof(wav_ref_table) / sizeof(wav_ref_table[0]);
const int n_async_chan = sizeof(csv_ref_table) / sizeof(csv_ref_table[0]);


/*  */
void print_ff(FILE *fileout, double round, double data) {
  if (round == 0) {
    fprintf(fileout, "%.0f", data);
  }
  else if (round == 4) {
    fprintf(fileout, "%.4f", data);
  }
  else if (round == 5) {
    fprintf(fileout, "%.5f", data);
  }
  else if (round == 8) {
    fprintf(fileout, "%.8f", data);
  }
}

void print_sf(char *line, double round, double data) {
  if (round == 0) {
    sprintf(line+ strlen(line), "%.0f", data);
  }
  else if (round == 4) {
    sprintf(line+ strlen(line), "%.4f", data);
  }
  else if (round == 5) {
    sprintf(line+ strlen(line), "%.5f", data);
  }
  else if (round == 8) {
    sprintf(line+ strlen(line), "%.8f", data);
  }
}



void print_wav_header(FILE *fileout, int chanIndex) {
  fprintf(fileout, "%s [%s] (/api/datatype/%i/),", wav_name[chanIndex][0], wav_name[chanIndex][3], (int)wav_ref_table[chanIndex][6]);
}

void print_csv_header(FILE *fileout, int chanIndex) {
  fprintf(fileout, "%s [%s] (/api/datatype/%i/),", csv_name[chanIndex][0], csv_name[chanIndex][3], (int)csv_ref_table[chanIndex][6]);
}

/*Convert all file at one Hz. If needed, put all results in the same file  */
int convert_1Hz_file(const char *dir, const char *dirout, int option, double start_s, int *converted) {
  char filename[512];
  char line[512];
  size_t fldcnt = 1;
  int fldcntSum = 1;
  unsigned short dataUnsigned;
  short dataSigned;
  double data;
  int i0 = 0;
  int i1 = 0;
  int i2 = 0;
  int n_file_in = 0;
  FILE* filesin[n_one_hz];
  FILE* fileout;
  int filecount = 0;
  unsigned long BUFSIZE = sizeof(dataUnsigned);
  int counter = 0;
  
  for(i0=0; i0< n_one_hz; i0++) {
    i1 = one_hz[i0];
    strcat(strcat(strcpy(filename, dir), wav_name[i1][0]), ".wav");
    filesin[i0] = fopen(filename, "r+b");
    if (filesin[i0] != NULL) {
      fseek(filesin[i0], 44, SEEK_SET);
      filecount++;
    }
  }
  if (filecount == 0) {
    return 1;
  }
  else if (dirout == NULL  && (option & HEADER)) {
    strcat(strcpy(filename, dir), "outputData.csv");
    fileout = fopen(filename, "w");}
  else if (dirout == NULL ) {
    strcat(strcpy(filename, dir), "outputData.csv");
    fileout = fopen(filename, "a");}
  else if (option & HEADER) {
    strcat(strcpy(filename, dirout), "outputData.csv");
    fileout = fopen(filename, "w");}
  else {
    strcat(strcpy(filename, dirout), "outputData.csv");
    fileout = fopen(filename, "a");
  }
  if (option & HEADER) {
    fprintf(fileout, "time [s],");
  }
  for(i0 = 0; i0 < n_one_hz; i0++) {
    if (filesin[i0] != NULL) {
      if (option & HEADER) {
        print_wav_header(fileout, one_hz[i0]);
      }
      n_file_in += 1;
      ++(*converted);
    }
  }
  if (option & HEADER) {
    fprintf(fileout, "\n");
  }
  
  while (fldcntSum > 0) {
    fldcntSum = 0;
    data = -1;
   memset(line, 0, sizeof(line));
    for (i0 = 0; i0 < n_one_hz; i0++) {
      i1 = one_hz[i0];
      fldcnt = 0;
      if (filesin[i0] != NULL) {
        if (wav_ref_table[i1][4]) {
          fldcnt = fread(&dataSigned, 1, BUFSIZE, filesin[i0]);
          data = (double)dataSigned*wav_ref_table[i1][2]+wav_ref_table[i1][3];
        }
        else {
          fldcnt = fread(&dataUnsigned, 1, BUFSIZE, filesin[i0]);
          data = (double)dataUnsigned*wav_ref_table[i1][2]+wav_ref_table[i1][3];
        }
        if (fldcntSum == 0 && fldcnt > 0) {
          sprintf(line + strlen(line), "%.8f,", start_s + (double)counter*wav_ref_table[i1][0] + wav_ref_table[i1][1]);
        }
        if (fldcnt > 0) {
          print_sf(line+ strlen(line), wav_ref_table[i1][5], data);
        }
        fldcntSum += (fldcnt? 1: 0);
        if (fldcntSum > 0){
          if (i0 != n_one_hz - 1) {
            sprintf(line + strlen(line), ",");
          }
          else {
            counter ++;
            sprintf(line + strlen(line), "\n");
          }
        }
      }
    }
    if (fldcntSum == n_file_in)//only save line if complete
      fputs(line, fileout);
  }
  for(i0 = 0; i0< n_one_hz; i0++) {
    if (filesin[i0] != NULL) {
      fclose(filesin[i0]);
    }
  }
  fclose(fileout);
  return 0;
}

int convert_hxd_file(const char *dir, const char *dirout, int chanIndex, int option, double start_s, int *converted) {
  char filename[512];
  long long unsigned int time;
  long long unsigned int data;
  unsigned long BUFSIZE = sizeof(time);
  char line [128];
  size_t fldcnt = 1;
  FILE *filein;
  FILE *fileout;
  strcat(strcat(strcpy(filename, dir), csv_name[chanIndex][0]), ".hxd");
  filein = fopen(filename, "r+b");
  if (filein == NULL) {
    return 0;
  }
  else if (dirout == NULL) {
    strcat(strcat(strcpy(filename, dir), csv_name[chanIndex][0]), ".csv");
    fileout = fopen(filename, "w");
  }
  else if (option & HEADER){
    strcat(strcat(strcpy(filename, dirout), csv_name[chanIndex][0]), ".csv");
    fileout = fopen(filename, "w");
  }
  else{
    strcat(strcat(strcpy(filename, dirout), csv_name[chanIndex][0]), ".csv");
    fileout = fopen(filename, "a");
  }
  if (line[0] != 't') {
    rewind(filein);
  }
  if (option & HEADER) {
    fprintf(fileout, "time [s],");
    print_csv_header(fileout, chanIndex);
    fprintf(fileout, "\n");
  }
  while (fldcnt > 0) {
    fldcnt = fread(&time, 1, BUFSIZE, filein);
    fldcnt += fread(&data, 1, BUFSIZE, filein);
    if (fldcnt) {
      fprintf(fileout, "%.8f,", start_s + time/256.);
      print_ff(fileout, csv_ref_table[chanIndex][5], data*csv_ref_table[chanIndex][2]+csv_ref_table[chanIndex][3]);
      fprintf(fileout, "\n");
    }
  }
  ++(*converted);
  fclose(filein);
  fclose(fileout);
  return 0;
}
int convert_csv_file(const char *dir,const char *dirout, int chanIndex, int option, double start_s, int *converted) {
  char filename[512];
  int counter = 1;
  double time;
  double data;
  char line [128];
  FILE *filein;
  FILE *fileout;

  
  strcat(strcat(strcpy(filename, dir), csv_name[chanIndex][0]), ".csv");
  filein = fopen(filename, "r");
  if (filein == NULL) {
    return 0;
  }
  else if (dirout == NULL && (option & EPOCH)) {
    strcat(strcat(strcpy(filename, dir), csv_name[chanIndex][1]), ".csv");
    fileout = fopen(filename, "w");
  }
  else if (dirout == NULL) {
    return 0;
  }
  else if ((option & HEADER) && (option & EPOCH)) {
    strcat(strcat(strcpy(filename, dirout), csv_name[chanIndex][1]), ".csv");
    fileout = fopen(filename, "w");
  }
  else if (option & EPOCH  ){
    strcat(strcat(strcpy(filename, dirout), csv_name[chanIndex][1]), ".csv");
    fileout = fopen(filename, "a");
  }
  else if ((option & HEADER) ) {
    strcat(strcat(strcpy(filename, dirout), csv_name[chanIndex][0]), ".csv");
    fileout = fopen(filename, "w");
  }
  else{
    strcat(strcat(strcpy(filename, dirout), csv_name[chanIndex][0]), ".csv");
    fileout = fopen(filename, "a");
  }
  fgets (line, sizeof line, filein);
  if (line[0] != 't') {
    rewind(filein);
  }
  if (option & HEADER) {
    fprintf(fileout, "time [s],");
    print_csv_header(fileout, chanIndex);
    fprintf(fileout, "\n");
  }
  while (counter > 0) {
    counter =fscanf(filein, "%le,%le", &time, &data);
    if (counter) {
      fprintf(fileout, "%.8f,", start_s + time );
      print_ff(fileout, 0, data);
      fprintf(fileout, "\n");
    }
  }
  ++(*converted);
  fclose(filein);
  fclose(fileout);
  return 0;
}


int convert_wave_file(const char *dir, const char *dirout, int chanIndex, int option, double start_s, int *converted) {
  char filename[512];
  int counter = 0;
  int add_quality;
  unsigned short dataUnsigned;
  short dataSigned;
  double data;
  unsigned long BUFSIZE = sizeof(dataUnsigned);
  size_t fldcnt = 1;
  FILE *filein;
  FILE *fileinqlty = NULL;
  FILE *fileout;
  strcat(strcat(strcpy(filename, dir), wav_name[chanIndex][0]), ".wav");
  filein = fopen(filename, "r+b");
  add_quality = (option & ADD_QUALITY) && strcmp(wav_name[chanIndex][2], "") != 0;
  if (option & GROUPED) {
    if (chanIndex == one_hz[0] && wav_ref_table[chanIndex][0] == 1) {
      convert_1Hz_file(dir, dirout, option, start_s, converted);
    }
    return 0;
  }
  else if (filein == NULL) {
    return 0;
  }
  else if ((option & ADD_QUALITY) && strcmp(wav_name[chanIndex][2], "NONE") == 0) { // skip quality signal
    return 0;
  }
  else if (add_quality) {
    strcat(strcat(strcpy(filename, dir), wav_name[chanIndex][2]), ".wav");
    fileinqlty = fopen(filename, "r+b");
    if (fileinqlty == NULL) { // add quality signal
      printf("quality signal file missing. Aborted\n");
      return 1;
    }
    fseek(fileinqlty, 44, SEEK_SET);
  }
  if (dirout == NULL) {
    strcat(strcat(strcpy(filename, dir), wav_name[chanIndex][1]), ".csv");
    fileout = fopen(filename, "w");
  }
  else if (option & HEADER) {
    strcat(strcat(strcpy(filename, dirout), wav_name[chanIndex][1]), ".csv");
    fileout = fopen(filename, "w");
  }
  else {
    strcat(strcat(strcpy(filename, dirout), wav_name[chanIndex][1]), ".csv");
    fileout = fopen(filename, "a");
  }
  fseek(filein, 44, SEEK_SET);
  if(option & HEADER) { //print header
    fprintf(fileout, "time [s],");
    print_wav_header(fileout, chanIndex);
    if (add_quality) {
      print_wav_header(fileout, chanIndex+1);
    }
    fprintf(fileout, "\n");
  }
  
  while (fldcnt > 0) { // parse and save data
    if (wav_ref_table[chanIndex][4]) {
      fldcnt = fread(&dataSigned, 1, BUFSIZE, filein);
      data = (double)dataSigned*wav_ref_table[chanIndex][2]+wav_ref_table[chanIndex][3];
    }
    else {
      fldcnt = fread(&dataUnsigned, 1, BUFSIZE, filein);
      data = (double)dataUnsigned*wav_ref_table[chanIndex][2]+wav_ref_table[chanIndex][3];
    }
    if (fldcnt > 0) {
      fprintf(fileout, "%.8f,", start_s + (double)counter*wav_ref_table[chanIndex][0] + wav_ref_table[chanIndex][1]);
      print_ff(fileout, wav_ref_table[chanIndex][5], data);
      if (add_quality && fileinqlty != NULL) {
        fldcnt = fread(&dataSigned, 1, BUFSIZE, fileinqlty);
        fprintf(fileout, ",%i\n", dataSigned);
      }
      else {
        fprintf(fileout, "\n");
      }
      counter ++;
    }
  }
  fclose(filein);
  fclose(fileout);
  if (fileinqlty != NULL) {
    fclose(fileinqlty);
  }
  ++(*converted);
  return 0;
}

int convert_sub_directory(const char *dirname,const char *dirnameout, int option, long long int start, int *converted) {
  int failed = 0;
  int i1;
  
  if (!(option & GROUPED)) { //run if we don't have option -group
    for (i1 = 0; i1 < n_async_chan; i1++) {
      failed += convert_csv_file(dirname, dirnameout, i1, option, (double)start/256, converted);
      failed += convert_hxd_file(dirname, dirnameout, i1, option, (double)start/256, converted);
    }
  }
  for (i1 = 0; i1 < n_wav_chan; i1++) {
    failed += convert_wave_file(dirname, dirnameout, i1, option, (double)start/256, converted);
  }
  return failed;
}

/*
 Look in directory or subdirectory to find files to convert
 */
int convert_directory(const char *directory, int option, int *converted) {
  char directory1[512];
  char text[512];
  long long int starts[256];
  char directories[256][512];
  int i = 0;
  int i_dir = 0;
  int j = 0;
  int k = 0;
  int file_converted_per_dir = 0;
  long long int start_sub_dir = 0;
  long long int start = 0;
  FILE *fileInfo;
  int failed = 0;
  
  strcat(strcpy(directory1, directory), "/");
  strcat(directory1, "/info.json");
  fileInfo = fopen(directory1, "r");
  if (fileInfo != NULL) {
    while (fgets(text, sizeof text, fileInfo) != NULL && i==0) {
      i = sscanf(text, "    \"start\": %lld", &start);
      if (i == 0) {
        i = sscanf(text, "    \"start_timestamp\": %lld", &start);
      }
    }
    if (i == 0) {
      printf("Could not decode start in %s. Aborted.",directory1);
      return 1;
    }
    else if (start <300000000000ll || start >400000000000ll) {
      printf("start_timestamp =%lli. out of range. Aborted.", start);
      return 1;
    }
  }
  else {
    
    printf("%s is missing. Please redownload. Aborted.", directory1);
    return 1;
  }
  
  // Check if one or many subdirectory can be converted
  tinydir_dir dir;
  tinydir_open(&dir, directory);
  while (dir.has_next) {
    tinydir_file file;
    tinydir_readfile(&dir, &file);
    if (file.is_dir && (strstr(file.name, "record_") != NULL)) {
      strcat(strcpy(directory1, directory), "/");
      strcat(directory1,file.name);
      strcat(directory1, "/info.json");
      fileInfo = fopen(directory1, "r");
      if (fileInfo != NULL) {
        i = 0;
        while (fgets(text, sizeof text, fileInfo) != NULL && i==0) {
          i = sscanf(text, "    \"start\": %lld", &start_sub_dir);
          if (i == 0) {
            i = sscanf(text, "    \"start_timestamp\": %lld", &start_sub_dir);
          }
        }
        if (i == 0) {
          printf("could not decode start in %s. Aborted.", directory1);
          return 1;
        } else if (!(option & EPOCH)) {
          start_sub_dir -= start;
        }
        for (j = 0; j < i_dir; j++) {
          if (starts[j] > start_sub_dir) {
            break;
          }
        }
        for (k = i_dir-1; k >= j; k--) {
          starts[k+1] = starts[k];
          strcpy(directories[k+1], directories[k]);
        }
        starts[k+1] = start_sub_dir;
        strcat(strcat(strcat(strcpy(directories[k+1], directory), "/"),file.name), "/");
        i_dir++;
      }
    }
    tinydir_next(&dir);
  }
  tinydir_close(&dir);
  
  
  if (i_dir > 0) {
    // Run conversion on all subdirectory
    strcat(strcpy(directory1, directory), "/");
    for (k = 0; k < i_dir; k++) {
      if (k == 0) {
        convert_sub_directory(directories[k], directory1, option, starts[k], converted);
      }
      else {
        convert_sub_directory(directories[k], directory1, option - (option & HEADER), starts[k], converted);
      }
      if (!(option & EPOCH)) {
        failed += convert_sub_directory(directories[k], NULL, option, 0, converted);
      }
      else {
        failed += convert_sub_directory(directories[k], NULL, option, starts[k], converted);
      }
      if (file_converted_per_dir ==0){
        file_converted_per_dir = *converted;
      }
      else if ((*converted%file_converted_per_dir != 0) && (option & GROUPED)){
        printf("Record subdirectories don't have the same number of files to decode. This may be due to a mix of synced and not synced data. Conversion aborted\n");
        *converted = 0;
        return 1;
      }
      
    }
  }
  else {
    if (!(option & EPOCH)) {
      start = 0; // if no epoch, offset is 0
    }
    // Run conversion on current directory
    strcat(strcpy(directory1, directory), "/");
    strcat(directory1, "/info.json");
    fileInfo = fopen(directory1, "r");
    strcat(strcpy(directory1, directory), "/");
    failed += convert_sub_directory(directory1, NULL, option, start , converted);
  }
  
  return failed;
}

/*
 Check if the conversion script is up to date with the files returned by the server
 */
int check_version(const char *fp) {
  char dirname[512];
  char text[512];
  int major;
  int minor;
  int micro;
  int i = 0;
  FILE *fileInfo;
  strcat(strcpy(dirname, fp), "/");
  strcat(dirname, "/info.json");
  fileInfo = fopen(dirname, "r");
  if (fileInfo != NULL) {
    while (fgets(text, sizeof text, fileInfo) != NULL && i==0) {
      i = sscanf(text, "    \"decoder_version\": \"%i.%i.%i", &major, &minor, &micro);
      if (i && major*256*256+minor*256+micro > MAJOR*256*256+MINOR*256+MICRO) {
        printf("Decoder version %i.%i.%i  too old. redownload decoder\n", MAJOR, MINOR, MICRO);
        return 1;
      }
    }
    if (i == 0) {
      printf("could not decode version number in %s. Please redownload data. Aborted", dirname);
      return 1;
    }
  }
  else {
    printf("%s. is missing, Please redownload. Aborted.", dirname);
    return 1;
  }
  return 0;
}



int main(int argc, const char * argv[]) {
  int add_quality = 0;
  int group = 0;
  int epoch = 0;
  int converted = 0;
  int failed;
  int header = HEADER;
  // option mask  1: add quality,   2: group      4: add header     8: save in epoch
  int i;
  struct stat s;
  int err;
  if (argc == 1) {
    printf("Convert wave to txt file\n");
    printf("Version %i.%i.%i\n", MAJOR, MINOR, MICRO);
    printf("Usage:   ConvertSourceFile directory [option]\n");
    printf("option:  -addquality  : add quality status to heartrate and breathingrate instead of putting them in separate files \n");
    printf("option:  -group       : all 1Hz signal in the same file \n");
    printf("option:  -epoch       : save in Posix epoch time. (seconds since 1 January 1970 00:00:00 UTC) \n");
    printf("option:  -noheader    : Don't save header\n");
    return 0;
  }
  else {
    if (argc >= 3) {
      for (i=2; i<argc; i++) {
        if( !(strcmp(argv[i], "-addquality") == 0 || strcmp(argv[i], "-group") == 0 || strcmp(argv[i], "-epoch") == 0 || strcmp(argv[i], "-noheader") == 0 )) {
          printf("Invalid option selected: %s. Aborted\n", argv[i]);
          return 1;
        }
        else if (strcmp(argv[i], "-epoch") == 0) {
          epoch = EPOCH;
        }
        else if (strcmp(argv[i], "-group") == 0) {
          group = GROUPED;
        }
        else if (strcmp(argv[i], "-addquality") == 0) {
          add_quality = ADD_QUALITY;
        }
        else if (strcmp(argv[i], "-noheader") == 0) {
          header = 0;
        }
      }
    }
    err = stat(argv[1], &s);
    if (err==-1|| !S_ISDIR(s.st_mode)) {
      printf("Not a valid directory. Aborted\n");
      return 1;
    }
    else if (group && add_quality) {
      printf("Cannot have simultanously options -addquality and -group. Aborted\n");
      return 1;
    }
    if (check_version(argv[1])) {
      return 1;
    }
    failed = convert_directory(argv[1], header +group + add_quality + epoch, &converted);
    printf("%i file converted\n", converted);
    if (failed == 0) {
      return 0;
    }
    else {
      return 1;
    }
  }
}


