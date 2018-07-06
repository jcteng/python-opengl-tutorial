#version 330
 
uniform mat4 MVP;
layout(location = 0) in vec3 vertexPosition_modelspace;
 
void main(void)
{
  gl_Position = MVP *vec4(vertexPosition_modelspace,1);
}