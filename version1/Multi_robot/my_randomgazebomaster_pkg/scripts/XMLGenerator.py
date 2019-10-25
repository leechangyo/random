#!/usr/bin/env python
import xml.etree.ElementTree as ET
import copy
import os
import shutil
import rospkg


class XMLObjectTags :
    def __init__(self, name, pose3d):
        """
        We get the Pose in 3D of the Center Of Mas of the object, XYZ and OrientationQuaternion XYZW
        and we convert it into XML tags.
        pose3d=[0,0,0,0,0,0,0]
        :param name:
        :param cof_and_bndbox:
        """
        self.root = ET.Element('object')
        self.subs = dict()
        self.subs['name'] = ET.SubElement(self.root,'name')
        self.subs['name'].text = name

        self.subs['pose3d'] = dict()
        self.subs['pose3d']['root'] = ET.SubElement(self.root, 'pose3d')
        self.subs['pose3d']['x_com'] = ET.SubElement(self.subs['pose3d']['root'],'x_com')
        self.subs['pose3d']['x_com'].text = str(pose3d[0])
        self.subs['pose3d']['y_com'] = ET.SubElement(self.subs['pose3d']['root'],'y_com')
        self.subs['pose3d']['y_com'].text = str(pose3d[1])
        self.subs['pose3d']['z_com'] = ET.SubElement(self.subs['pose3d']['root'],'z_com')
        self.subs['pose3d']['z_com'].text = str(pose3d[2])
        self.subs['pose3d']['quat_x'] = ET.SubElement(self.subs['pose3d']['root'],'quat_x')
        self.subs['pose3d']['quat_x'].text = str(pose3d[3])
        self.subs['pose3d']['quat_y'] = ET.SubElement(self.subs['pose3d']['root'], 'quat_y')
        self.subs['pose3d']['quat_y'].text = str(pose3d[4])
        self.subs['pose3d']['quat_z'] = ET.SubElement(self.subs['pose3d']['root'], 'quat_z')
        self.subs['pose3d']['quat_z'].text = str(pose3d[5])
        self.subs['pose3d']['quat_w'] = ET.SubElement(self.subs['pose3d']['root'], 'quat_w')
        self.subs['pose3d']['quat_w'].text = str(pose3d[6])



    def getRoot(self):
        return self.root


class XMLGenerator:
    def __init__(self, path_out='./'):

        # get an instance of RosPack with the default search paths
        rospack = rospkg.RosPack()
        # get the file path for rospy_tutorials

        path_to_package = rospack.get_path('my_randomgazebomaster_pkg')
        XML_dir = "XMLGenerator"
        base_file_name = "base_annotation.xml"

        path_to_scripts = os.path.join(path_to_package, "scripts")
        #path_to_XMLdir = os.path.join(path_to_scripts, XML_dir)
        #path_to_base_annotation = os.path.join(path_to_XMLdir, base_file_name)
        path_to_base_annotation = os.path.join(path_to_scripts, base_file_name)
        self.et_base = ET.parse(path_to_base_annotation)

        self.path_out = path_out+'_annotations/'

        if os.path.exists(self.path_out):
            shutil.rmtree(self.path_out)

        os.makedirs(self.path_out)

    def generate(self, object_tags, filename='filename', extension_file=".png", camera_width=640, camera_height=480):
        et = copy.deepcopy(self.et_base)
        root = et.getroot()
        root.find('filename').text = filename + extension_file

        size_elem = root.find('size')
        width_elem = ET.SubElement(size_elem, "width")
        width_elem.text = str(camera_width)
        height_elem = ET.SubElement(size_elem, "height")
        height_elem.text = str(camera_height)

        for obj in object_tags:
            root.append(obj.getRoot())

        et.write('{}{}.xml'.format(self.path_out, filename))
