#version 330
 
layout(location = 0) in vec2 UV;
 
void main(void)
{
  gl_Position = vec4(UV,0,1);
}