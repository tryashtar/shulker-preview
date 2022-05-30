#version 150

#moj_import <fog.glsl>

in vec3 Position;
in vec4 Color;
in vec2 UV0;
in ivec2 UV2;

uniform sampler2D Sampler2;

uniform mat4 ModelViewMat;
uniform mat4 ProjMat;
uniform mat3 IViewRotMat;
uniform int FogShape;

out float vertexDistance;
out vec4 vertexColor;
out vec2 texCoord0;

flat out int modelID;
flat out int faces;
out vec2 screenPos;
out vec3 cornerTex1;
out vec3 cornerTex2;
flat out vec3 cornerTex3;

vec2[] corners = vec2[](
    vec2(-1.0, 1.0),
    vec2(-1.0,-1.0),
    vec2( 1.0,-1.0),
    vec2( 1.0, 1.0)
);

const float size = 4;
const vec2 offset = vec2(-2, -1);

void main() {

    vec3 pos = Position;

    // Get the selected model's ID into one number
    modelID = -1;
    faces = -1;
    if (int(Color.b * 255.) == 0xfc) {
        modelID = int(Color.r * 255.);
        faces = int(Color.g * 255.);
        pos.xy += offset + size * (vec2(1.0, -1.0) * corners[gl_VertexID % 4]*.5 + .5);
    }

    if (int(Color.r * 255.) == 0x3f && int(Color.g * 255.) == 0x3f && int(Color.b * 255.) == 0x3d) {
        pos.y -= 20;
        pos.x += 4;
    }

    // Output the position on the character
    screenPos = corners[gl_VertexID % 4];

    // Output the edges of the UV coordinates to know where the character is (credits to Bálint)
    cornerTex1 = vec3(0);
    cornerTex2 = vec3(0);
    cornerTex3 = vec3(0);
    if (gl_VertexID % 4 == 0) cornerTex1 = vec3(UV0, 1);
    if (gl_VertexID % 4 == 2) cornerTex2 = vec3(UV0, 1);
    if (gl_VertexID % 2 == 1) cornerTex3 = vec3(UV0, 1);

    gl_Position = ProjMat * ModelViewMat * vec4(pos, 1.0);

    vertexDistance = fog_distance(ModelViewMat, IViewRotMat * pos, FogShape);
    vertexColor = Color * texelFetch(Sampler2, UV2 / 16, 0);
    texCoord0 = UV0;
}
