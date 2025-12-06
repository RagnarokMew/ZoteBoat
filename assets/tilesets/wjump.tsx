<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.10" tiledversion="1.11.2" name="wjump" tilewidth="128" tileheight="128" tilecount="3" columns="0">
 <grid orientation="orthogonal" width="1" height="1"/>
 <tile id="0">
  <properties>
   <property name="side" type="int" value="-1"/>
  </properties>
  <image source="../sprites/icons/left.png" width="80" height="80"/>
  <objectgroup draworder="index" id="3">
   <object id="2" x="100" y="0" width="8" height="80"/>
  </objectgroup>
 </tile>
 <tile id="1">
  <properties>
   <property name="side" type="int" value="1"/>
  </properties>
  <image source="../sprites/icons/right.png" width="80" height="80"/>
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="0" width="8" height="80"/>
  </objectgroup>
 </tile>
 <tile id="2">
  <properties>
   <property name="side" type="int" value="0"/>
  </properties>
  <image source="../sprites/icons/noEntry.png" width="128" height="128"/>
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="0" width="128" height="128"/>
  </objectgroup>
 </tile>
</tileset>
