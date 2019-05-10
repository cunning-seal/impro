from PIL import Image, ExifTags
import sys
import os


class App:


    def __init__(self, dir_name: str):
        self.files = sorted(os.listdir(dir_name))

        self.dir_name = dir_name + "/"


        self.preprocess_dir = "preprocessed_files"

    def create_pdf(self, result_name: str):
        image_list = []

        im1 = Image.open(self.dir_name + self.files[0])
        for im in self.files[1:]:
            image_list.append(Image.open(self.dir_name + im))

        im1.save(result_name, "PDF", resolution=100.0, save_all=True, append_images=image_list)

    # TODO создавать папку для препроцессных файлов + добавить состояние (исходная папка/препроцессная папка)
    def preprocessing(self):
        """
        Rotating all pictures in work directory as it should be
        :return:
        """
        for file in self.files:
            try:
                name = self.dir_name + "/" + file
                image = Image.open(name)
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = dict(image._getexif().items())

                if exif[orientation] == 3:
                    image = image.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    image = image.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    image = image.rotate(90, expand=True)
                image.save("preprocessed_files/" + file)
                image.close()

            except (AttributeError, KeyError, IndexError):
                # cases: image don't have getexif
                pass

        self.dir_name = self.preprocess_dir

    def __del__(self):
        try:
            for root, dirs, files in os.walk(self.preprocess_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
        except:
            return

if __name__ == '__main__':
    a = App(sys.argv[1])
    a.preprocessing()
    a.create_pdf(sys.argv[2])