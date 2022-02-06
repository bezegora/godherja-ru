import cv2
import numpy as np
import re
import configparser
import os
import sys
import shutil

class Province_Image():
    def __init__(self, image_path):
        print("Reading province image...")
        image_data = cv2.imread(image_path)
        image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)
        image_data = image_data.reshape(-1, image_data.shape[-1])
        image_data = image_data.tolist()
        self.unique_data = [list(x) for x in set(tuple(x) for x in image_data)]
        print("Read province image...")

    def Find_unique_colors(self, province_existing_colors):
        print("Finding new provinces...")
        self.final_unique_colors = []
        for value in self.unique_data:
            if province_existing_colors.count(value) > 0:
                continue
            self.final_unique_colors.append(value)
        print("Found new provinces...")

class Province_Defs():
    def __init__(self, def_path):
        print("Reading definitions .csv...")
        self.main_path = def_path
        with open(def_path, newline='') as defs:
            defs_read = defs.read() + '\n'
            regex_search = re.compile("(?<=;)[0-9]+;[0-9]+;[0-9]+")
            matched_colors = re.findall(regex_search, defs_read)
            self.final_results = []
            for string in matched_colors:
                result = string.split(";")
                for i, v in enumerate(result):
                    result[i] = int(v)
                self.final_results.append(result)

            find_last_province = re.compile("(?<=\n)[0-9]+")
            self.last_province = re.findall(find_last_province, defs_read)
            self.last_province = int(self.last_province[len(self.last_province)-1])
            line_grabber = re.compile(".+\n")
            re_checked = re.findall(line_grabber, defs_read)
            self.titles_list = []
            for value in re_checked:
                self.titles_list.append(value.split(";")[4])
            print("Read definitions .csv...")
    
    def Write_to_csv(self, unique_data):
        print("Writing to definition.csv...")
        with open(self.main_path, "a") as final_csv:
            seperator = ";"
            counter = 0
            for data in unique_data:
                self.last_province += 1
                counter += 1
                formatter = str(self.last_province)
                final_csv.write(f"\n{formatter};{seperator.join([str(v) for v in data])};b_test_{formatter};x;")
        print(f"{counter} provinces added. New total is {self.last_province}...")

class Landed_Titles():
    def __init__(self, filepath):
        self.title_number = 0
        self.filler_title_exists = True
        self.title_filepath = filepath
        with open(filepath) as landed_titles_json:
            self.filler_title_exists = True
            landed_titles_read = landed_titles_json.read()
            self.full_txt = landed_titles_read
            check_for_placeholder = re.compile("(?<=\n)e_fill.*?(?<=\n)}", re.RegexFlag.DOTALL | re.RegexFlag.IGNORECASE)
            self.filler_title = re.findall(check_for_placeholder, landed_titles_read)
            if len(self.filler_title) == 0:
                print("No filler title found in script. Will make new one...")
                self.filler_title_exists = False

            # TODO: this is a no good terrible way to do this. find a better way -wrongend 9/11/2020
        with open(filepath) as landed_titles_json:
            read_lines = landed_titles_json.readlines()
            # TODO: This is extremely slow. Find a faster way to do it. -wrongend 9/11/2020
            number_checker = re.compile("(?<= = )[0-9]+")
            self.title_number = re.findall(number_checker, str(read_lines))
            self.title_number = max([int(x) for x in self.title_number])

    def Generate_color_association_tuple(self, finished_def_list):
        with open(finished_def_list) as def_list:
            list_grabber = re.compile("(?<=;)[0-9]+;[0-9]+;[0-9]+;.+(?=;x)")
            associated_list = re.findall(list_grabber, def_list.read())
            self.associated_tuples = []
            for value in associated_list:
                final = tuple(value.split(";"))
                self.associated_tuples.append(final)

    def Find_used_b_titles(self, list_of_titles_in_csv):
        self.unique_titles = []
        for title in list_of_titles_in_csv:
            # TODO: write a proper stack parser for this. -wrongend 9/11/2020
            if title[3] not in self.full_txt:
                self.unique_titles.append(title)
    
    def Append_unused_titles(self, list_of_unused_titles):
        # TODO: we need to assume something better than "The filler is at the direct bottom" -wrongend 9/11/2020
        # TODO: Stack overflow to the rescue. Find a better way to do this. -wrongend 9/12/2020
        shutil.copy2(self.title_filepath, "temp.txt")
        if self.filler_title_exists:
            for i in range(5):
                with open("temp.txt", "rb+") as file:

                    # Move the pointer (similar to a cursor in a text editor) to the end of the file
                    file.seek(0, os.SEEK_END)

                    # This code means the following code skips the very last character in the file -
                    # i.e. in the case the last line is null we delete the last line
                    # and the penultimate one
                    pos = file.tell() - 1

                    # Read each character in the file one at a time from the penultimate
                    # character going backwards, searching for a newline character
                    # If we find a new line, exit the search
                    while pos > 0 and file.read(1) != b"\n":
                        pos -= 1
                        file.seek(pos, os.SEEK_SET)

                    # So long as we're not at the start of the file, delete all the characters ahead
                    # of this position
                    if pos > 0:
                        file.seek(pos, os.SEEK_SET)
                        file.truncate()

        with open("temp.txt", "a") as temp:
            if not self.filler_title_exists:
                temp.write("""\ne_fill = {
    color = { 219 190 44 }
    color2 = { 255 255 23 }

    k_fill = {
        color = { 219 190 44 }
        color2 = { 255 255 23 }
        
        d_fill = {
            color = { 219 190 44 }
            color2 = { 255 255 255 }
            
            c_fill = {
                color = { 219 190 44 }
                color2 = { 255 255 255 }
                """)
            count = 0
            for title in list_of_unused_titles:
                count += 1
                self.title_number += 1
                temp.write("\n")
                temp.write("\n               %s = {" % title[3])
                temp.write("\n                    province = %s" % self.title_number)
                temp.write("\n")
                temp.write("\n                    color = { %s %s %s }" % (title[0], title[1], title[2]))
                temp.write("\n                    color2 = { 255 255 255 }")
                temp.write("\n				}")
            temp.write("""
            }
        }
    }
}""")
            #self.final_write = self.read_file
            form_count = str(count)
            form_title_number = str(self.title_number)
            print(f"Added {form_count} new baronies to the filler title. New count of baronies is {form_title_number}.")

        shutil.copy2("temp.txt", self.title_filepath)
        os.unlink("temp.txt")



        


            
                

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("automapper.ini")
    worker = Province_Image(config["filepaths"]["province_image"])
    worker1 = Province_Defs(config["filepaths"]["definition_csv"])
    worker.Find_unique_colors(worker1.final_results)
    worker1.Write_to_csv(worker.final_unique_colors)
    worker3 = Landed_Titles(config["filepaths"]["landed_titles"])
    worker3.Generate_color_association_tuple(config["filepaths"]["definition_csv"])
    worker3.Find_used_b_titles(worker3.associated_tuples)
    worker3.Append_unused_titles(worker3.unique_titles)

