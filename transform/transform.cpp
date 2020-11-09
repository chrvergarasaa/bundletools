#include <stdio.h>
#include <stdlib.h>
#include <cstdio>
#include <cstring>
#include <math.h>
#include <unordered_map>
#include "dirent.h"
#include <sys/stat.h>
#include <algorithm>
#include <fstream>
#include <string>
#include <vector>
#include <iostream>
#include <cmath>

using namespace std;

char * str_to_char_array(string s){
    int length = s.length()+1;
    char * char_array = new char[length];
#pragma omp parallel for
    for (unsigned short int i = 0; i<=length;i++){
        char_array[i] = s[i];
    }
    return char_array;
}

void read_bundles(const string &path, uint16_t &nBundles, uint32_t *&nFibers, uint16_t **&nPoints, float ****&Points) {

	vector<string> bundlesDir;

	DIR *dir;
	struct dirent *ent;
	if((dir = opendir(path.c_str())) != NULL) {
	  /* get all the file names and directories within directory */
	  while((ent = readdir (dir)) != NULL) {
	    const string bundle_dir = ent->d_name;
	    if(*bundle_dir.rbegin() == 'a')
	    	bundlesDir.emplace_back(path + bundle_dir);
	  }
	  closedir (dir);
	}
	else {
	  /* could not open directory */
	  perror("Error");
	  exit( EXIT_FAILURE );
	}

	sort(bundlesDir.begin(), bundlesDir.end());

	nBundles = bundlesDir.size();

	nFibers = new uint32_t[nBundles];
	nPoints = new uint16_t*[nBundles];
	Points = new float***[nBundles];

	for(uint16_t i=0; i<nBundles; i++) {

		string filename = bundlesDir[i];
		ifstream file(filename, ios::in | ios::binary);

		if(file.is_open()) {

			streampos fsize = 0;
			file.seekg( 0, ios::end );
			uint32_t num = (file.tellg() - fsize) / 4;
			file.seekg( 0 );

			uint32_t num_count = 0;

			vector<uint32_t> nPointsList;
			vector<float**> PointsList;

			while( num_count < num ) {

				uint32_t total_points; // number of points of each fiber
				file.read ((char*)&total_points, sizeof(uint32_t));

				float **Fiber = new float*[total_points]; // fiber

				for(uint32_t k=0; k<total_points; k++) {
					Fiber[k] = new float[3];

					for(uint8_t m = 0; m < 3; m++)
						file.read ((char *) & Fiber[k][m], sizeof(float));
				}

				num_count = num_count + 1 + ( total_points * 3 );
				nPointsList.emplace_back(total_points);
				PointsList.emplace_back(Fiber);
			}

			nFibers[i] = nPointsList.size();
			nPoints[i] = new uint16_t[nPointsList.size()];
			Points[i] = new float**[nPointsList.size()];

			//cout << nFibers[0] << endl;

			for(uint32_t j=0; j<nPointsList.size(); j++) {
				nPoints[i][j] = nPointsList[j];
				Points[i][j] = PointsList[j];
			}

		//	cout << nPointsList.size() << endl;	
		}
		file.close();
	}
}

void apply_trm(string path, uint16_t &nBundles, uint32_t *&nFibers, uint16_t **&nPoints, float ****&Points){

	char path2[path.length()+1];
    strncpy(path2, path.c_str(), sizeof(path2));
    path2[sizeof(path2) - 1] = 0;
    FILE *fp = fopen(path2, "r");
	 // Open subject file.
    if (fp == NULL) {fputs ("File error opening file\n",stderr); exit (1);}

    float fm[12];

    unsigned int i = 0;

    while(!feof(fp)){
    	if (fscanf(fp, "%f ", &fm[i]));
    	i++;
    }

    float matrix[4][4] = {fm[3],fm[4],fm[5],fm[0],fm[6],fm[7],fm[8],fm[1],fm[9],fm[10],fm[11],fm[2],0,0,0,1};
    
    for (unsigned int z = 0; z < nBundles; z++){
	    for(unsigned int i = 0; i < nFibers[z]; i++){
	    	for(unsigned int j = 0; j < nPoints[z][i]; j++){
	    		float pad_points[4] = {Points[z][i][j][0],Points[z][i][j][1],Points[z][i][j][2],1};
				for(unsigned int k = 0; k < 4; k++){
					float acum = 0;
					for(unsigned int l = 0; l < 4; l++){
						acum += matrix[k][l] * pad_points[l];
					}

					if(k < 3){
						Points[z][i][j][k] = acum;	
					}
				}
	    	}
	    }
    }
}


void write_bundles(const string &pathBundles, const std::string output_path, uint32_t *&nFibers, uint16_t **&nPoints, float ****&Points){
	
	std::vector<std::string> bundlesDir;

	DIR *dirInt;
	struct dirent *ent;
	if((dirInt = opendir(pathBundles.c_str())) != NULL) {
	  /* get all the file names and directories within directory */
	  while((ent = readdir (dirInt)) != NULL) {
	    const std::string bundle_dir = ent->d_name;
	    if(*bundle_dir.rbegin() == 's')
	    	bundlesDir.emplace_back(bundle_dir.substr(0,bundle_dir.size() - 8));
	  }
	  closedir (dirInt);
	}
	else {
	  /* could not open directory */
	  perror("Error");
	  exit( EXIT_FAILURE );
	}

	std::sort(bundlesDir.begin(), bundlesDir.end());

	ofstream bundlesfile;
	struct stat sb;
    char * output_folder = str_to_char_array(output_path);
    if (stat(output_folder, &sb) == 0 && S_ISDIR(sb.st_mode)){
        char * command =  str_to_char_array("rm -r "+output_path);
        int del = system(command);
    }
    mkdir(output_folder, S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);

    for(unsigned int z = 0; z < bundlesDir.size(); z++){
    	//std::cout << bundlesDir[z] << std::endl;
    	string bundlesdata_path = output_path + bundlesDir[z] + "_trm.bundlesdata";
	    char * bundlesdata_file = str_to_char_array(bundlesdata_path);
	    FILE *fp = fopen(bundlesdata_file, "wb"); 	// Opening and writing .bundlesdata file.
	    if (fp == NULL) {fputs ("File error opening .bundlesdata file\n",stderr); exit (1);}

	    for (unsigned int i = 0; i < nFibers[z] ; i++) {
	        fwrite(&nPoints[z][i], sizeof(uint16_t),1, fp);

	        uint16_t pad = 0;
	        fwrite(&pad, sizeof(uint16_t), 1, fp);
	        
	        for (unsigned int j = 0; j < nPoints[z][i]; j++){
	    		for (unsigned int k = 0; k < 3; k++){
					Points[z][i][j][k] = Points[z][i][j][k];
					fwrite(&Points[z][i][j][k], sizeof(float), 1, fp);		
	    		} 
	        }
	    }

	    fclose(fp);

	    bundlesfile.open( output_path + bundlesDir[z] + "_trm.bundles", ios::out);
	    bundlesfile<< "attributes = {"<<endl
	               <<"    \'binary\' : 1,"<<endl
	               <<"    \'bundles\' : ['points', 0]," << endl
	               <<"    \'byte_order\' : \'DCBA\',"<<endl
	               <<"    \'curves_count\' : "<<nFibers[z]<<","<< endl
	               <<"    \'data_file_name\' : \'*.bundlesdata\',"<<endl
	               <<"    \'format\' : \'bundles_1.0\',"<<endl
	               <<"    \'space_dimension\' : 3"<<endl
	               <<"  }"<<endl;
	    bundlesfile.close();
	    delete(bundlesdata_file);
    }	
}


int main(int argc, char const *argv[])
{
	uint16_t nBundles;
	uint32_t *nFibers;
	uint16_t **nPoints;
	float ****Points;

	read_bundles(argv[1], nBundles, nFibers, nPoints, Points);
	apply_trm(argv[3], nBundles, nFibers, nPoints, Points);
	write_bundles(argv[1], argv[2], nFibers, nPoints, Points);

	return 0;
}