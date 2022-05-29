#version 150

#moj_import <fog.glsl>

uniform sampler2D Sampler0;

uniform vec4 ColorModulator;
uniform float FogStart;
uniform float FogEnd;
uniform vec4 FogColor;

in float vertexDistance;
in vec4 vertexColor;
in vec2 texCoord0;

flat in int modelID;
in vec2 screenPos;
in vec3 cornerTex1;
in vec3 cornerTex2;
flat in vec3 cornerTex3;

out vec4 fragColor;

vec4 getUV() {
    vec2 cornerUV1 = cornerTex1.xy / cornerTex1.z;
    vec2 cornerUV2 = cornerTex2.xy / cornerTex2.z;
    vec2 cornerUV3 = cornerTex3.xy / cornerTex3.z;
    vec2 minUV = min(cornerUV1, min(cornerUV2, cornerUV3));
    vec2 maxUV = max(cornerUV1, max(cornerUV2, cornerUV3));
    return vec4(minUV, maxUV);
}

bool handleIntersection(vec2 intersection, vec2 flip, vec4 uvMinMax, vec3 normal, int rotation) {
    if (0.0 <= intersection.x && intersection.x <= 1.0 && 0.0 <= intersection.y && intersection.y <= 1.0) {
        switch (rotation) {
            case 0:
                break;
            case 90:
                intersection.xy = intersection.yx;
                flip.y = 1. - flip.y;
                break;
            case 180:
                flip = 1. - flip;
                break;
            case 270:
                intersection.xy = intersection.yx;
                flip.x = 1. - flip.x;
                break;
        }
        intersection = flip - (flip * 2. - 1.) * intersection;
        vec2 UV = mix(uvMinMax.xy, uvMinMax.zw, intersection);
        fragColor = texture(Sampler0, UV);
        fragColor.rgb *= dot(normal, vec3(102., 255., 166.)/255.);
        if (fragColor.a < 0.1)
            discard;
        return true;
    }
    return false;
}

vec4 mapUV(vec4 uv, vec4 minmax) {
    return mix(minmax.xyxy, minmax.zwzw, uv.xyzw / 16.0);
}

/**
 * Calculates the ray-plane intersection with an axis-aligned cuboid and writes to `fragColor`.
 * faces: A bitmap to determine which faces are rendered.
 *        bit 0: Render face pointing towards Y-axis (up)
 *        bit 1: Render face pointing towards X-axis (east)
 *        bit 2: Render face pointing towards Z-axis (north)
 * rd: The direction that the ray points in.
 * ro: The origin of the ray.
 * from: The same as `from` in an item model.
 * to: The same as `to` in an item model.
 * uvX: The same as `uv` in an item model for the face pointing towards X-axis (east)
 * uvY: The same as `uv` in an item model for the face pointing towards Y-axis (up)
 * uvZ: The same as `uv` in an item model for the face pointing towards Z-axis (north)
 * uvRange: Value returned by getUV()
 * t: The depth at which the cuboid is hit. Only written to if an intersection occurs.
 * This method returns whether an intersection occurred.
**/
bool cuboid(int faces, vec3 rd, vec3 ro, vec3 from, vec3 to, vec4 uvX, int rotX, vec4 uvY, int rotY, vec4 uvZ, int rotZ, vec4 uvRange, out float t) {
    from /= 16.0;
    to /= 16.0;
    vec3 size = to - from;
    // y
    float tY = (to.y - ro.y)/rd.y;
    if ((faces      & 1) == 1 && handleIntersection(((rd * tY + ro).xz - from.xz)/size.xz, vec2(0.0, 0.0), mapUV(uvY, uvRange), vec3(0.0, 1.0, 0.0), (rotY + 90) % 360)) {
        t = tY;
        return true;
    }
    // x
    float tX = (to.x - ro.x)/rd.x;
    if ((faces >> 1 & 1) == 1 && handleIntersection(((rd * tX + ro).zy - from.zy)/size.zy, vec2(1.0, 1.0), mapUV(uvX, uvRange), vec3(1.0, 0.0, 0.0), rotX)) {
        t = tX;
        return true;
    }
    // z
    float tZ = (to.z - ro.z)/rd.z;
    if ((faces >> 2 & 1) == 1 && handleIntersection(((rd * tZ + ro).xy - from.xy)/size.xy, vec2(0.0, 1.0), mapUV(uvZ, uvRange), vec3(0.0, 0.0, 1.0), rotZ)) {
        t = tZ;
        return true;
    }
    return false;
}

vec3[] tints = vec3[](
    vec3(252., 252., 252.),
    vec3(123., 187., 106.),
    vec3( 96., 151.,  96.)
);

bool block_cube(int modelID, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float t;
    bool hit = cuboid(modelID, rd, ro, vec3(0.0), vec3(16.0), vec4(0, 0, 16, 16), 0, vec4(0, 0, 16, 16), 0, vec4(0, 0, 16, 16), 0, uvRange, t);
    fragColor.rgb *= tints[(modelID / 8)] / 255.;
    return hit;
}

bool block_slab(vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float t;
    return cuboid(7, rd, ro, vec3(0.0), vec3(16.0, 8.0, 16.0), vec4(0, 0, 16, 8), 0, vec4(0, 0, 16, 16), 0, vec4(0, 0, 16, 8), 0, uvRange, t);
}

bool block_fence(vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float postT;
    bool hitPost = cuboid( // left post
        7, rd, ro, 
        vec3(6.0, 0.0, 0.0), vec3(10.0, 16.0, 4.0), // from, to
        vec4(0, 0, 4, 16), 0, vec4(6, 0, 10, 4), 270, vec4(6, 0, 10, 16), 0, // east UV, up UV, north UV
        uvRange, postT) || cuboid( // right post
        7, rd, ro, 
        vec3(6.0, 0.0, 12.0), vec3(10.0, 16.0, 16.0),
        vec4(12, 0, 16, 16), 0, vec4(6, 12, 10, 16), 270, vec4(6, 0, 10, 16), 0,
        uvRange, postT);
    vec4 postCol = fragColor;
    float barT;
    bool hitBar = cuboid( // top bar
        7, rd, ro,
        vec3(7.0, 13.0, -2.0), vec3(9.0, 15.0, 18.0),
        vec4(0, 1, 16, 3), 0, vec4(7, 0, 9, 16), 270, vec4(7, 1, 9, 3), 0,
        uvRange, barT) || cuboid( // bottom bar
        7, rd, ro,
        vec3(7, 5, -2), vec3(9, 7, 18),
        vec4(0, 9, 16, 11), 0, vec4(7, 0, 9, 16), 270, vec4(7, 9, 9, 11), 0,
        uvRange, barT);
    if (hitPost && hitBar) {
        if (postT < barT)
            fragColor = postCol;
    }
    return hitPost || hitBar;
}

bool custom_block(int modelID, vec3 rd, vec3 ro) {
    switch (modelID) {
        case 24: // Fence model
            return block_fence(rd, ro);
        case 25:
            return block_slab(rd, ro);
    }
    return false;
}

void main() {
    if (modelID != -1) {
        // Get ray properties (ray direction, ray origin)
        vec3 rd = normalize(vec3(-1, -0.804, -1));
        vec3 localX = normalize(cross(vec3(0.0, 1.0, 0.0), rd));
        vec3 localY = normalize(cross(rd, localX));
        vec3 ro = (-localX * screenPos.x + localY * screenPos.y);

        // Calculate ray plane intersections
        if (modelID / 8 < tints.length()) {
            if (block_cube(modelID, rd, ro)) return;
            else discard;
        }
        if (custom_block(modelID, rd, ro)) return;
        else discard;
    }
    vec4 color = texture(Sampler0, texCoord0) * vertexColor * ColorModulator;
    if (color.a < 0.1) {
        discard;
    }
    fragColor = linear_fog(color, vertexDistance, FogStart, FogEnd, FogColor);
}
