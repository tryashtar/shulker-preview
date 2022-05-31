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
flat in int faces;
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
    if ((faces >> 2 & 1) == 1 && handleIntersection(((rd * tX + ro).zy - from.zy)/size.zy, vec2(1.0, 1.0), mapUV(uvX, uvRange), vec3(1.0, 0.0, 0.0), rotX)) {
        t = tX;
        return true;
    }
    // z
    float tZ = (to.z - ro.z)/rd.z;
    if ((faces >> 1 & 1) == 1 && handleIntersection(((rd * tZ + ro).xy - from.xy)/size.xy, vec2(0.0, 1.0), mapUV(uvZ, uvRange), vec3(0.0, 0.0, 1.0), rotZ)) {
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

bool block_cube(int modelID, int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float t;
    bool hit = cuboid(faces, rd, ro, vec3(0.0), vec3(16.0), vec4(0, 0, 16, 16), 0, vec4(0, 0, 16, 16), 0, vec4(0, 0, 16, 16), 0, uvRange, t);
    fragColor.rgb *= tints[(modelID / 8)] / 255.;
    return hit;
}


// custom blocks start
// from minecraft:block/cube
bool block_1(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 16.0, 16.0), vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0;
}
// from minecraft:block/snow_height2
bool block_2(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 2.0, 16.0), vec4(0.0, 14.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 14.0, 16.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0;
}
// from minecraft:block/template_anvil
bool block_3(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(2.0, 0.0, 2.0), vec3(14.0, 4.0, 14.0), vec4(4.0, 2.0, 0.0, 14.0), 270, vec4(2.0, 2.0, 14.0, 14.0), 180, vec4(2.0, 12.0, 14.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(4.0, 4.0, 3.0), vec3(12.0, 5.0, 13.0), vec4(5.0, 3.0, 4.0, 13.0), 270, vec4(4.0, 3.0, 12.0, 13.0), 180, vec4(4.0, 11.0, 12.0, 12.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube2 = cuboid(faces, rd, ro, vec3(6.0, 5.0, 4.0), vec3(10.0, 10.0, 12.0), vec4(10.0, 4.0, 5.0, 12.0), 270, vec4(6.0, 4.0, 10.0, 12.0), 0, vec4(6.0, 6.0, 10.0, 11.0), 0, uvRange, t);
    if (cube2 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube3 = cuboid(faces, rd, ro, vec3(3.0, 10.0, 0.0), vec3(13.0, 16.0, 16.0), vec4(16.0, 0.0, 10.0, 16.0), 270, vec4(3.0, 0.0, 13.0, 16.0), 180, vec4(3.0, 0.0, 13.0, 6.0), 0, uvRange, t);
    if (cube3 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1 || cube2 || cube3;
}
// from fake:chest
bool block_4(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(7.0, 7.0, 0.0), vec3(9.0, 11.0, 1.0), vec4(1.0, 1.25, 0.75, 0.25), 0, vec4(1.25, 0.25, 0.75, 0.0), 0, vec4(1.5, 1.25, 1.0, 0.25), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(1.0, 9.0, 1.0), vec3(15.0, 14.0, 15.0), vec4(10.5, 4.75, 7.0, 3.5), 0, vec4(10.5, 0.0, 7.0, 3.5), 0, vec4(14.0, 4.75, 10.5, 3.5), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube2 = cuboid(faces, rd, ro, vec3(1.0, 0.0, 1.0), vec3(15.0, 10.0, 15.0), vec4(10.5, 10.75, 7.0, 8.25), 0, vec4(10.5, 4.75, 7.0, 8.25), 0, vec4(14.0, 10.75, 10.5, 8.25), 0, uvRange, t);
    if (cube2 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1 || cube2;
}
// from minecraft:block/template_azalea
bool block_5(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 16.0, 0.0), vec3(16.0, 16.0, 16.0), vec4(0.0, 0.0, 16.0, 0.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 0.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(0.0, 5.0, 0.0), vec3(16.0, 16.0, 0.01), vec4(15.99, 0.0, 16.0, 11.0), 0, vec4(0.0, 0.0, 16.0, 0.01), 0, vec4(0.0, 0.0, 16.0, 11.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube2 = cuboid(faces, rd, ro, vec3(0.0, 5.0, 15.99), vec3(16.0, 16.0, 16.0), vec4(0.0, 0.0, 0.009999999999999787, 11.0), 0, vec4(0.0, 15.99, 16.0, 16.0), 0, vec4(16.0, 0.0, 0.0, 11.0), 0, uvRange, t);
    if (cube2 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube3 = cuboid(faces, rd, ro, vec3(0.0, 5.0, 0.0), vec3(0.01, 16.0, 16.0), vec4(16.0, 0.0, 0.0, 11.0), 0, vec4(0.0, 0.0, 0.01, 16.0), 0, vec4(15.99, 0.0, 16.0, 11.0), 0, uvRange, t);
    if (cube3 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube4 = cuboid(faces, rd, ro, vec3(15.99, 5.0, 0.0), vec3(16.0, 16.0, 16.0), vec4(0.0, 0.0, 16.0, 11.0), 0, vec4(15.99, 0.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 0.009999999999999787, 11.0), 0, uvRange, t);
    if (cube4 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube5 = cuboid(faces, rd, ro, vec3(0.1, 0.0, 8.0), vec3(15.9, 15.9, 8.0), vec4(8.0, 0.09999999999999964, 8.0, 16.0), 0, vec4(0.1, 8.0, 15.9, 8.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, uvRange, t);
    if (cube5 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube6 = cuboid(faces, rd, ro, vec3(8.0, 0.0, 0.1), vec3(8.0, 15.9, 15.9), vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(8.0, 0.1, 8.0, 15.9), 0, vec4(8.0, 0.09999999999999964, 8.0, 16.0), 0, uvRange, t);
    if (cube6 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1 || cube2 || cube3 || cube4 || cube5 || cube6;
}
// from minecraft:block/beacon
bool block_6(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 16.0, 16.0), vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(2.0, 0.1, 2.0), vec3(14.0, 3.0, 14.0), vec4(2.0, 13.0, 14.0, 16.0), 0, vec4(2.0, 2.0, 14.0, 14.0), 0, vec4(2.0, 13.0, 14.0, 16.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube2 = cuboid(faces, rd, ro, vec3(3.0, 3.0, 3.0), vec3(13.0, 14.0, 13.0), vec4(3.0, 2.0, 13.0, 13.0), 0, vec4(3.0, 3.0, 13.0, 13.0), 0, vec4(3.0, 2.0, 13.0, 13.0), 0, uvRange, t);
    if (cube2 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1 || cube2;
}
// from minecraft:block/cactus
bool block_7(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 16.0, 16.0), vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 1.0), vec3(16.0, 16.0, 15.0), vec4(1.0, 0.0, 15.0, 16.0), 0, vec4(0.0, 1.0, 16.0, 15.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube2 = cuboid(faces, rd, ro, vec3(1.0, 0.0, 0.0), vec3(15.0, 16.0, 16.0), vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(1.0, 0.0, 15.0, 16.0), 0, vec4(1.0, 0.0, 15.0, 16.0), 0, uvRange, t);
    if (cube2 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1 || cube2;
}
// from minecraft:block/cube_directional
bool block_8(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 16.0, 16.0), vec4(0.0, 0.0, 16.0, 16.0), 90, vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0;
}
// from fake:conduit
bool block_9(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(5.0, 5.0, 5.0), vec3(11.0, 11.0, 11.0), vec4(9.0, 12.0, 6.0, 6.0), 0, vec4(6.0, 6.0, 9.0, 0.0), 0, vec4(6.0, 12.0, 3.0, 6.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0;
}
// from minecraft:block/end_rod
bool block_10(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(6.0, 0.0, 6.0), vec3(10.0, 1.0, 10.0), vec4(2.0, 6.0, 6.0, 7.0), 0, vec4(2.0, 2.0, 6.0, 6.0), 0, vec4(2.0, 6.0, 6.0, 7.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(7.0, 1.0, 7.0), vec3(9.0, 16.0, 9.0), vec4(0.0, 0.0, 2.0, 15.0), 0, vec4(2.0, 0.0, 4.0, 2.0), 0, vec4(0.0, 0.0, 2.0, 15.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1;
}
// from minecraft:block/lectern
bool block_11(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 2.0, 16.0), vec4(0.0, 6.0, 16.0, 8.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 180, vec4(0.0, 14.0, 16.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(4.0, 2.0, 4.0), vec3(12.0, 15.0, 12.0), vec4(2.0, 16.0, 15.0, 8.0), 90, vec4(4.0, 4.0, 12.0, 12.0), 0, vec4(0.0, 0.0, 8.0, 13.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube2 = cuboid(faces, rd, ro, vec3(0.0125, 12.0, 3.0), vec3(15.9875, 16.0, 16.0), vec4(0.0, 4.0, 13.0, 8.0), 0, vec4(0.0, 1.0, 16.0, 14.0), 180, vec4(0.0, 0.0, 16.0, 4.0), 0, uvRange, t);
    if (cube2 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1 || cube2;
}
// from fake:red_bed
bool block_12(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(13.0, 0.0, 0.0), vec3(16.0, 3.0, 3.0), vec4(12.5, 5.25, 13.25, 6.0), 0, vec4(13.25, 4.5, 14.0, 5.25), 0, vec4(13.25, 5.25, 14.0, 6.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(0.0, 3.0, 16.0), vec3(16.0, 9.0, 32.0), vec4(5.5, 7.0, 7.0, 11.0), 90, vec4(1.5, 7.0, 5.5, 11.0), 0, vec4(0.0, 7.0, 16.0, 13.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube2 = cuboid(faces, rd, ro, vec3(13.0, 0.0, 29.0), vec3(16.0, 3.0, 32.0), vec4(13.25, 3.75, 14.0, 4.5), 0, vec4(13.25, 3.0, 14.0, 3.75), 270, vec4(14.0, 3.75, 14.75, 4.5), 0, uvRange, t);
    if (cube2 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube3 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 29.0), vec3(3.0, 3.0, 32.0), vec4(14.0, 0.75, 14.75, 1.5), 0, vec4(13.25, 0.0, 14.0, 0.75), 180, vec4(14.75, 0.75, 15.5, 1.5), 0, uvRange, t);
    if (cube3 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube4 = cuboid(faces, rd, ro, vec3(0.0, 3.0, 0.0), vec3(16.0, 9.0, 16.0), vec4(5.5, 1.5, 7.0, 5.5), 90, vec4(1.5, 1.5, 5.5, 5.5), 0, vec4(1.5, 0.0, 5.5, 1.5), 180, uvRange, t);
    if (cube4 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube5 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(3.0, 3.0, 3.0), vec4(14.75, 2.25, 15.5, 3.0), 0, vec4(13.25, 1.5, 14.0, 2.25), 90, vec4(12.5, 2.25, 13.25, 3.0), 0, uvRange, t);
    if (cube5 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1 || cube2 || cube3 || cube4 || cube5;
}
// from minecraft:block/template_farmland
bool block_13(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 15.0, 16.0), vec4(0.0, 1.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 1.0, 16.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0;
}
// from minecraft:block/slab
bool block_14(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 8.0, 16.0), vec4(0.0, 8.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 8.0, 16.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0;
}
// from minecraft:block/observer
bool block_15(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 16.0, 16.0), vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 16.0, 16.0, 0.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0;
}
// from minecraft:block/composter
bool block_16(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 2.0, 16.0), vec4(0.0, 14.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 14.0, 16.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(2.0, 16.0, 16.0), vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 2.0, 16.0), 0, vec4(14.0, 0.0, 16.0, 16.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube2 = cuboid(faces, rd, ro, vec3(14.0, 0.0, 0.0), vec3(16.0, 16.0, 16.0), vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(14.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 2.0, 16.0), 0, uvRange, t);
    if (cube2 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube3 = cuboid(faces, rd, ro, vec3(2.0, 0.0, 0.0), vec3(14.0, 16.0, 2.0), vec4(14.0, 0.0, 16.0, 16.0), 0, vec4(2.0, 0.0, 14.0, 2.0), 0, vec4(2.0, 0.0, 14.0, 16.0), 0, uvRange, t);
    if (cube3 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube4 = cuboid(faces, rd, ro, vec3(2.0, 0.0, 14.0), vec3(14.0, 16.0, 16.0), vec4(0.0, 0.0, 2.0, 16.0), 0, vec4(2.0, 14.0, 14.0, 16.0), 0, vec4(2.0, 0.0, 14.0, 16.0), 0, uvRange, t);
    if (cube4 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1 || cube2 || cube3 || cube4;
}
// from minecraft:block/fence_inventory
bool block_17(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(6.0, 0.0, 0.0), vec3(10.0, 16.0, 4.0), vec4(0.0, 0.0, 4.0, 16.0), 0, vec4(6.0, 0.0, 10.0, 4.0), 0, vec4(6.0, 0.0, 10.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(6.0, 0.0, 12.0), vec3(10.0, 16.0, 16.0), vec4(12.0, 0.0, 16.0, 16.0), 0, vec4(6.0, 12.0, 10.0, 16.0), 0, vec4(6.0, 0.0, 10.0, 16.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube2 = cuboid(faces, rd, ro, vec3(7.0, 12.0, 0.0), vec3(9.0, 15.0, 16.0), vec4(0.0, 1.0, 16.0, 4.0), 0, vec4(7.0, 0.0, 9.0, 16.0), 0, vec4(7.0, 1.0, 9.0, 4.0), 0, uvRange, t);
    if (cube2 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube3 = cuboid(faces, rd, ro, vec3(7.0, 12.0, -2.0), vec3(9.0, 15.0, 0.0), vec4(0.0, 1.0, 2.0, 4.0), 0, vec4(7.0, 14.0, 9.0, 16.0), 0, vec4(7.0, 1.0, 9.0, 4.0), 0, uvRange, t);
    if (cube3 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube4 = cuboid(faces, rd, ro, vec3(7.0, 12.0, 16.0), vec3(9.0, 15.0, 18.0), vec4(14.0, 1.0, 16.0, 4.0), 0, vec4(7.0, 0.0, 9.0, 2.0), 0, vec4(7.0, 1.0, 9.0, 4.0), 0, uvRange, t);
    if (cube4 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube5 = cuboid(faces, rd, ro, vec3(7.0, 6.0, 0.0), vec3(9.0, 9.0, 16.0), vec4(0.0, 7.0, 16.0, 10.0), 0, vec4(7.0, 0.0, 9.0, 16.0), 0, vec4(7.0, 7.0, 9.0, 10.0), 0, uvRange, t);
    if (cube5 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube6 = cuboid(faces, rd, ro, vec3(7.0, 6.0, -2.0), vec3(9.0, 9.0, 0.0), vec4(0.0, 7.0, 2.0, 10.0), 0, vec4(7.0, 14.0, 9.0, 16.0), 0, vec4(7.0, 7.0, 9.0, 10.0), 0, uvRange, t);
    if (cube6 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube7 = cuboid(faces, rd, ro, vec3(7.0, 6.0, 16.0), vec3(9.0, 9.0, 18.0), vec4(14.0, 7.0, 16.0, 10.0), 0, vec4(7.0, 0.0, 9.0, 2.0), 0, vec4(7.0, 7.0, 9.0, 10.0), 0, uvRange, t);
    if (cube7 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1 || cube2 || cube3 || cube4 || cube5 || cube6 || cube7;
}
// from minecraft:block/wall_inventory
bool block_18(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(4.0, 0.0, 4.0), vec3(12.0, 16.0, 12.0), vec4(4.0, 0.0, 12.0, 16.0), 0, vec4(4.0, 4.0, 12.0, 12.0), 0, vec4(4.0, 0.0, 12.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(5.0, 0.0, 0.0), vec3(11.0, 13.0, 16.0), vec4(0.0, 3.0, 16.0, 16.0), 0, vec4(5.0, 0.0, 11.0, 16.0), 0, vec4(5.0, 3.0, 11.0, 16.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1;
}
// from minecraft:block/dragon_egg
bool block_19(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(6.0, 15.0, 6.0), vec3(10.0, 16.0, 10.0), vec4(6.0, 15.0, 10.0, 16.0), 0, vec4(6.0, 6.0, 10.0, 10.0), 0, vec4(6.0, 15.0, 10.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(5.0, 14.0, 5.0), vec3(11.0, 15.0, 11.0), vec4(5.0, 14.0, 11.0, 15.0), 0, vec4(5.0, 5.0, 11.0, 11.0), 0, vec4(5.0, 14.0, 11.0, 15.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube2 = cuboid(faces, rd, ro, vec3(5.0, 13.0, 5.0), vec3(11.0, 14.0, 11.0), vec4(4.0, 13.0, 12.0, 14.0), 0, vec4(4.0, 4.0, 12.0, 12.0), 0, vec4(4.0, 13.0, 12.0, 14.0), 0, uvRange, t);
    if (cube2 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube3 = cuboid(faces, rd, ro, vec3(3.0, 11.0, 3.0), vec3(13.0, 13.0, 13.0), vec4(3.0, 11.0, 13.0, 13.0), 0, vec4(3.0, 3.0, 13.0, 13.0), 0, vec4(3.0, 11.0, 13.0, 13.0), 0, uvRange, t);
    if (cube3 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube4 = cuboid(faces, rd, ro, vec3(2.0, 8.0, 2.0), vec3(14.0, 11.0, 14.0), vec4(2.0, 8.0, 14.0, 11.0), 0, vec4(2.0, 2.0, 14.0, 14.0), 0, vec4(2.0, 8.0, 14.0, 11.0), 0, uvRange, t);
    if (cube4 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube5 = cuboid(faces, rd, ro, vec3(1.0, 3.0, 1.0), vec3(15.0, 8.0, 15.0), vec4(1.0, 3.0, 15.0, 8.0), 0, vec4(1.0, 1.0, 15.0, 15.0), 0, vec4(1.0, 3.0, 15.0, 8.0), 0, uvRange, t);
    if (cube5 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube6 = cuboid(faces, rd, ro, vec3(2.0, 1.0, 2.0), vec3(14.0, 3.0, 14.0), vec4(2.0, 1.0, 14.0, 3.0), 0, vec4(2.0, 2.0, 14.0, 14.0), 0, vec4(2.0, 1.0, 14.0, 3.0), 0, uvRange, t);
    if (cube6 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube7 = cuboid(faces, rd, ro, vec3(3.0, 0.0, 3.0), vec3(13.0, 1.0, 13.0), vec4(3.0, 0.0, 13.0, 1.0), 0, vec4(3.0, 3.0, 13.0, 13.0), 0, vec4(3.0, 0.0, 13.0, 1.0), 0, uvRange, t);
    if (cube7 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1 || cube2 || cube3 || cube4 || cube5 || cube6 || cube7;
}
// from minecraft:block/grindstone
bool block_20(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(12.0, 0.0, 6.0), vec3(14.0, 7.0, 10.0), vec4(10.0, 16.0, 6.0, 9.0), 0, vec4(12.0, 6.0, 14.0, 10.0), 0, vec4(2.0, 9.0, 4.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(2.0, 0.0, 6.0), vec3(4.0, 7.0, 10.0), vec4(10.0, 16.0, 6.0, 9.0), 0, vec4(2.0, 6.0, 4.0, 10.0), 0, vec4(12.0, 9.0, 14.0, 16.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube2 = cuboid(faces, rd, ro, vec3(12.0, 7.0, 5.0), vec3(14.0, 13.0, 11.0), vec4(0.0, 0.0, 6.0, 6.0), 0, vec4(8.0, 0.0, 10.0, 6.0), 0, vec4(6.0, 0.0, 8.0, 6.0), 0, uvRange, t);
    if (cube2 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube3 = cuboid(faces, rd, ro, vec3(2.0, 7.0, 5.0), vec3(4.0, 13.0, 11.0), vec4(5.0, 3.0, 11.0, 9.0), 0, vec4(8.0, 0.0, 10.0, 6.0), 0, vec4(6.0, 0.0, 8.0, 6.0), 0, uvRange, t);
    if (cube3 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube4 = cuboid(faces, rd, ro, vec3(4.0, 4.0, 2.0), vec3(12.0, 16.0, 14.0), vec4(0.0, 0.0, 12.0, 12.0), 0, vec4(0.0, 0.0, 8.0, 12.0), 0, vec4(0.0, 0.0, 8.0, 12.0), 0, uvRange, t);
    if (cube4 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1 || cube2 || cube3 || cube4;
}
// from minecraft:block/button_inventory
bool block_21(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(5.0, 6.0, 6.0), vec3(11.0, 10.0, 10.0), vec4(6.0, 12.0, 10.0, 16.0), 0, vec4(5.0, 10.0, 11.0, 6.0), 0, vec4(5.0, 12.0, 11.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0;
}
// from minecraft:block/stairs
bool block_22(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 8.0, 16.0), vec4(0.0, 8.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 8.0, 16.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(8.0, 8.0, 0.0), vec3(16.0, 16.0, 16.0), vec4(0.0, 0.0, 16.0, 8.0), 0, vec4(8.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 8.0, 8.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1;
}
// from fake:red_banner
bool block_23(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(7.33333, 0.0, 7.33333), vec3(8.66666, 28.0, 8.66666), vec4(11.0, 0.5, 11.5, 11.0), 0, vec4(11.5, 0.0, 12.0, 0.5), 0, vec4(11.5, 0.5, 12.0, 11.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(1.33333, 28.0, 7.33333), vec3(14.66667, 29.33333, 8.66667), vec4(0.0, 11.0, 0.5, 11.5), 0, vec4(5.5, 11.0, 0.5, 10.5), 0, vec4(6.0, 11.0, 11.0, 11.5), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube2 = cuboid(faces, rd, ro, vec3(1.33333, 2.66667, 6.33333), vec3(14.66667, 29.33333, 7.33333), vec4(0.0, 0.25, 0.25, 10.25), 0, vec4(5.25, 0.0, 0.25, 0.25), 0, vec4(0.25, 0.25, 5.25, 10.25), 0, uvRange, t);
    if (cube2 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1 || cube2;
}
// from minecraft:block/carpet
bool block_24(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 1.0, 16.0), vec4(0.0, 15.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 15.0, 16.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0;
}
// from fake:dragon_head
bool block_25(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(2.0, 4.0, -14.0), vec3(14.0, 9.0, 2.0), vec4(11.0, 3.75, 12.0, 4.0625), 0, vec4(12.75, 3.75, 12.0, 2.75), 0, vec4(12.0, 3.75, 12.75, 4.0625), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 16.0, 16.0), vec4(7.0, 2.875, 8.0, 3.875), 0, vec4(9.0, 2.875, 8.0, 1.875), 0, vec4(8.0, 2.875, 9.0, 3.875), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube2 = cuboid(faces, rd, ro, vec3(11.0, 16.0, 6.0), vec3(13.0, 20.0, 12.0), vec4(0.875, 0.375, 0.5, 0.625), 0, vec4(0.375, 0.375, 0.5, 0.0), 0, vec4(0.5, 0.375, 0.375, 0.625), 0, uvRange, t);
    if (cube2 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube3 = cuboid(faces, rd, ro, vec3(11.0, 9.0, -12.0), vec3(13.0, 11.0, -8.0), vec4(7.625, 0.25, 7.375, 0.375), 0, vec4(7.25, 0.25, 7.375, 0.0), 0, vec4(7.375, 0.25, 7.25, 0.375), 0, uvRange, t);
    if (cube3 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube4 = cuboid(faces, rd, ro, vec3(3.0, 16.0, 6.0), vec3(5.0, 20.0, 12.0), vec4(0.0, 0.375, 0.375, 0.625), 0, vec4(0.5, 0.375, 0.375, 0.0), 0, vec4(0.375, 0.375, 0.5, 0.625), 0, uvRange, t);
    if (cube4 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube5 = cuboid(faces, rd, ro, vec3(3.0, 9.0, -12.0), vec3(5.0, 11.0, -8.0), vec4(7.0, 0.25, 7.25, 0.375), 0, vec4(7.375, 0.25, 7.25, 0.0), 0, vec4(7.25, 0.25, 7.375, 0.375), 0, uvRange, t);
    if (cube5 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube6 = cuboid(faces, rd, ro, vec3(2.0, 0.0, -14.0), vec3(14.0, 4.0, 2.0), vec4(11.0, 5.0625, 12.0, 5.3125), 0, vec4(12.75, 5.0625, 12.0, 4.0625), 0, vec4(12.0, 5.0625, 12.75, 5.3125), 0, uvRange, t);
    if (cube6 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1 || cube2 || cube3 || cube4 || cube5 || cube6;
}
// from minecraft:block/grass_block
bool block_26(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 16.0, 16.0), vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 16.0, 16.0), vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1;
}
// from minecraft:block/honey_block
bool block_27(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 16.0, 16.0), vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(1.0, 1.0, 1.0), vec3(15.0, 15.0, 15.0), vec4(1.0, 1.0, 15.0, 15.0), 0, vec4(1.0, 1.0, 15.0, 15.0), 0, vec4(1.0, 1.0, 15.0, 15.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1;
}
// from fake:player_head
bool block_28(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(4.0, 0.0, 4.0), vec3(12.0, 8.0, 12.0), vec4(0.0, 2.0, 2.0, 4.0), 0, vec4(4.0, 2.0, 2.0, 0.0), 0, vec4(2.0, 2.0, 4.0, 4.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(3.5, -0.5, 3.5), vec3(12.5, 8.5, 12.5), vec4(8.0, 2.0, 10.0, 4.0), 0, vec4(12.0, 2.0, 10.0, 0.0), 0, vec4(10.0, 2.0, 12.0, 4.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1;
}
// from minecraft:block/scaffolding_stable
bool block_29(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 15.99, 0.0), vec3(16.0, 16.0, 16.0), vec4(0.0, 0.0, 16.0, 0.009999999999999787), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 0.009999999999999787), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(2.0, 16.0, 2.0), vec4(14.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 2.0, 2.0), 0, vec4(14.0, 0.0, 16.0, 16.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube2 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 14.0), vec3(2.0, 16.0, 16.0), vec4(0.0, 0.0, 2.0, 16.0), 0, vec4(0.0, 14.0, 2.0, 16.0), 0, vec4(14.0, 0.0, 16.0, 16.0), 0, uvRange, t);
    if (cube2 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube3 = cuboid(faces, rd, ro, vec3(14.0, 0.0, 14.0), vec3(16.0, 16.0, 16.0), vec4(0.0, 0.0, 2.0, 16.0), 0, vec4(14.0, 14.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 2.0, 16.0), 0, uvRange, t);
    if (cube3 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube4 = cuboid(faces, rd, ro, vec3(14.0, 0.0, 0.0), vec3(16.0, 16.0, 2.0), vec4(14.0, 0.0, 16.0, 16.0), 0, vec4(14.0, 0.0, 16.0, 2.0), 0, vec4(0.0, 0.0, 2.0, 16.0), 0, uvRange, t);
    if (cube4 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube5 = cuboid(faces, rd, ro, vec3(2.0, 14.0, 0.0), vec3(14.0, 16.0, 2.0), vec4(14.0, 0.0, 16.0, 2.0), 0, vec4(2.0, 0.0, 14.0, 2.0), 0, vec4(2.0, 0.0, 14.0, 2.0), 0, uvRange, t);
    if (cube5 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube6 = cuboid(faces, rd, ro, vec3(2.0, 14.0, 14.0), vec3(14.0, 16.0, 16.0), vec4(0.0, 0.0, 2.0, 2.0), 0, vec4(2.0, 14.0, 14.0, 16.0), 0, vec4(14.0, 0.0, 2.0, 2.0), 0, uvRange, t);
    if (cube6 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube7 = cuboid(faces, rd, ro, vec3(14.0, 14.0, 2.0), vec3(16.0, 16.0, 14.0), vec4(14.0, 0.0, 2.0, 2.0), 0, vec4(14.0, 2.0, 16.0, 14.0), 0, vec4(0.0, 0.0, 2.0, 2.0), 0, uvRange, t);
    if (cube7 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube8 = cuboid(faces, rd, ro, vec3(0.0, 14.0, 2.0), vec3(2.0, 16.0, 14.0), vec4(2.0, 0.0, 14.0, 2.0), 0, vec4(0.0, 2.0, 2.0, 14.0), 0, vec4(14.0, 0.0, 16.0, 2.0), 0, uvRange, t);
    if (cube8 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1 || cube2 || cube3 || cube4 || cube5 || cube6 || cube7 || cube8;
}
// from fake:shulker_box
bool block_30(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 4.0, 0.0), vec3(16.0, 16.0, 16.0), vec4(8.0, 4.0, 12.0, 7.0), 0, vec4(4.0, 0.0, 8.0, 4.0), 0, vec4(12.0, 4.0, 16.0, 7.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 8.0, 16.0), vec4(8.0, 11.0, 12.0, 13.0), 0, vec4(4.0, 7.0, 8.0, 11.0), 0, vec4(12.0, 11.0, 16.0, 13.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1;
}
// from minecraft:block/slime_block
bool block_31(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(3.0, 3.0, 3.0), vec3(13.0, 13.0, 13.0), vec4(3.0, 3.0, 13.0, 13.0), 0, vec4(3.0, 3.0, 13.0, 13.0), 0, vec4(3.0, 3.0, 13.0, 13.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 16.0, 16.0), vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1;
}
// from minecraft:block/stonecutter
bool block_32(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 9.0, 16.0), vec4(0.0, 7.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 7.0, 16.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(1.0, 9.0, 8.0), vec3(15.0, 16.0, 8.0), vec4(8.0, 0.0, 8.0, 7.0), 0, vec4(1.0, 8.0, 15.0, 8.0), 0, vec4(1.0, 9.0, 15.0, 16.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1;
}
// from minecraft:block/big_dripleaf
bool block_33(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 15.0, 0.0), vec3(16.0, 15.0, 16.0), vec4(0.0, 1.0, 16.0, 1.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 1.0, 16.0, 1.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(0.0, 11.0, 0.0), vec3(16.0, 15.0, 0.002), vec4(15.998, 1.0, 16.0, 5.0), 0, vec4(0.0, 0.0, 16.0, 0.002), 0, vec4(0.0, 0.0, 16.0, 4.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube2 = cuboid(faces, rd, ro, vec3(0.0, 11.0, 0.0), vec3(0.002, 15.0, 16.0), vec4(16.0, 0.0, 0.0, 4.0), 0, vec4(0.0, 0.0, 0.002, 16.0), 0, vec4(15.998, 1.0, 16.0, 5.0), 0, uvRange, t);
    if (cube2 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube3 = cuboid(faces, rd, ro, vec3(15.998, 11.0, 0.0), vec3(16.0, 15.0, 16.0), vec4(16.0, 0.0, 0.0, 4.0), 0, vec4(15.998, 0.0, 16.0, 16.0), 0, vec4(0.0, 1.0, 0.002000000000000668, 5.0), 0, uvRange, t);
    if (cube3 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube4 = cuboid(faces, rd, ro, vec3(5.0, 0.0, 12.0), vec3(11.0, 15.0, 12.0), vec4(4.0, 1.0, 4.0, 16.0), 0, vec4(5.0, 12.0, 11.0, 12.0), 0, vec4(3.0, 0.0, 14.0, 16.0), 0, uvRange, t);
    if (cube4 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube5 = cuboid(faces, rd, ro, vec3(5.0, 0.0, 12.0), vec3(11.0, 15.0, 12.0), vec4(4.0, 1.0, 4.0, 16.0), 0, vec4(5.0, 12.0, 11.0, 12.0), 0, vec4(3.0, 0.0, 14.0, 16.0), 0, uvRange, t);
    if (cube5 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1 || cube2 || cube3 || cube4 || cube5;
}
// from minecraft:block/chorus_plant
bool block_34(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(2.0, 14.0, 2.0), vec3(14.0, 16.0, 14.0), vec4(2.0, 0.0, 14.0, 2.0), 0, vec4(2.0, 2.0, 14.0, 14.0), 0, vec4(2.0, 0.0, 14.0, 2.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(0.0, 2.0, 2.0), vec3(2.0, 14.0, 14.0), vec4(2.0, 2.0, 14.0, 14.0), 0, vec4(0.0, 2.0, 2.0, 14.0), 0, vec4(14.0, 2.0, 16.0, 14.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube2 = cuboid(faces, rd, ro, vec3(2.0, 2.0, 0.0), vec3(14.0, 14.0, 2.0), vec4(14.0, 2.0, 16.0, 14.0), 0, vec4(2.0, 0.0, 14.0, 2.0), 0, vec4(2.0, 2.0, 14.0, 14.0), 0, uvRange, t);
    if (cube2 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube3 = cuboid(faces, rd, ro, vec3(2.0, 2.0, 14.0), vec3(14.0, 14.0, 16.0), vec4(0.0, 2.0, 2.0, 14.0), 0, vec4(2.0, 14.0, 14.0, 16.0), 0, vec4(2.0, 2.0, 14.0, 14.0), 0, uvRange, t);
    if (cube3 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube4 = cuboid(faces, rd, ro, vec3(14.0, 2.0, 2.0), vec3(16.0, 14.0, 14.0), vec4(2.0, 2.0, 14.0, 14.0), 0, vec4(14.0, 2.0, 16.0, 14.0), 0, vec4(0.0, 2.0, 2.0, 14.0), 0, uvRange, t);
    if (cube4 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube5 = cuboid(faces, rd, ro, vec3(2.0, 0.0, 2.0), vec3(14.0, 2.0, 14.0), vec4(2.0, 14.0, 14.0, 16.0), 0, vec4(2.0, 2.0, 14.0, 14.0), 0, vec4(2.0, 14.0, 14.0, 16.0), 0, uvRange, t);
    if (cube5 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube6 = cuboid(faces, rd, ro, vec3(2.0, 2.0, 2.0), vec3(14.0, 14.0, 14.0), vec4(2.0, 2.0, 14.0, 14.0), 0, vec4(2.0, 2.0, 14.0, 14.0), 0, vec4(2.0, 2.0, 14.0, 14.0), 0, uvRange, t);
    if (cube6 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1 || cube2 || cube3 || cube4 || cube5 || cube6;
}
// from fake:creeper_head
bool block_35(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(4.0, 0.0, 4.0), vec3(12.0, 8.0, 12.0), vec4(0.0, 4.0, 2.0, 8.0), 0, vec4(4.0, 4.0, 2.0, 0.0), 0, vec4(2.0, 4.0, 4.0, 8.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(3.5, -0.5, 3.5), vec3(12.5, 8.5, 12.5), vec4(8.0, 4.0, 10.0, 8.0), 0, vec4(12.0, 4.0, 10.0, 0.0), 0, vec4(10.0, 4.0, 12.0, 8.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1;
}
// from minecraft:block/template_trapdoor_bottom
bool block_36(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 3.0, 16.0), vec4(0.0, 16.0, 16.0, 13.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 16.0, 16.0, 13.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0;
}
// from minecraft:block/sculk_sensor
bool block_37(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 8.0, 16.0), vec4(0.0, 8.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 8.0, 16.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(-1.0, 8.0, 3.0), vec3(7.0, 16.0, 3.0), vec4(13.0, 0.0, 13.0, 8.0), 0, vec4(-1.0, 3.0, 7.0, 3.0), 0, vec4(4.0, 8.0, 12.0, 16.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube2 = cuboid(faces, rd, ro, vec3(9.0, 8.0, 3.0), vec3(17.0, 16.0, 3.0), vec4(13.0, 0.0, 13.0, 8.0), 0, vec4(9.0, 3.0, 17.0, 3.0), 0, vec4(12.0, 8.0, 4.0, 16.0), 0, uvRange, t);
    if (cube2 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube3 = cuboid(faces, rd, ro, vec3(9.0, 8.0, 13.0), vec3(17.0, 16.0, 13.0), vec4(3.0, 0.0, 3.0, 8.0), 0, vec4(9.0, 13.0, 17.0, 13.0), 0, vec4(12.0, 8.0, 4.0, 16.0), 0, uvRange, t);
    if (cube3 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube4 = cuboid(faces, rd, ro, vec3(-1.0, 8.0, 13.0), vec3(7.0, 16.0, 13.0), vec4(3.0, 0.0, 3.0, 8.0), 0, vec4(-1.0, 13.0, 7.0, 13.0), 0, vec4(4.0, 8.0, 12.0, 16.0), 0, uvRange, t);
    if (cube4 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1 || cube2 || cube3 || cube4;
}
// from minecraft:block/template_chorus_flower
bool block_38(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(2.0, 14.0, 2.0), vec3(14.0, 16.0, 14.0), vec4(2.0, 0.0, 14.0, 2.0), 0, vec4(2.0, 2.0, 14.0, 14.0), 0, vec4(2.0, 0.0, 14.0, 2.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(0.0, 2.0, 2.0), vec3(2.0, 14.0, 14.0), vec4(2.0, 2.0, 14.0, 14.0), 0, vec4(0.0, 2.0, 2.0, 14.0), 0, vec4(14.0, 2.0, 16.0, 14.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube2 = cuboid(faces, rd, ro, vec3(2.0, 2.0, 0.0), vec3(14.0, 14.0, 2.0), vec4(14.0, 2.0, 16.0, 14.0), 0, vec4(2.0, 0.0, 14.0, 2.0), 0, vec4(2.0, 2.0, 14.0, 14.0), 0, uvRange, t);
    if (cube2 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube3 = cuboid(faces, rd, ro, vec3(2.0, 2.0, 14.0), vec3(14.0, 14.0, 16.0), vec4(0.0, 2.0, 2.0, 14.0), 0, vec4(2.0, 14.0, 14.0, 16.0), 0, vec4(2.0, 2.0, 14.0, 14.0), 0, uvRange, t);
    if (cube3 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube4 = cuboid(faces, rd, ro, vec3(14.0, 2.0, 2.0), vec3(16.0, 14.0, 14.0), vec4(2.0, 2.0, 14.0, 14.0), 0, vec4(14.0, 2.0, 16.0, 14.0), 0, vec4(0.0, 2.0, 2.0, 14.0), 0, uvRange, t);
    if (cube4 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube5 = cuboid(faces, rd, ro, vec3(2.0, 0.0, 2.0), vec3(14.0, 14.0, 14.0), vec4(2.0, 2.0, 14.0, 16.0), 0, vec4(2.0, 2.0, 14.0, 14.0), 0, vec4(2.0, 2.0, 14.0, 16.0), 0, uvRange, t);
    if (cube5 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1 || cube2 || cube3 || cube4 || cube5;
}
// from minecraft:block/lightning_rod
bool block_39(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(6.0, 12.0, 6.0), vec3(10.0, 16.0, 10.0), vec4(0.0, 0.0, 4.0, 4.0), 0, vec4(4.0, 4.0, 0.0, 0.0), 0, vec4(0.0, 0.0, 4.0, 4.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(7.0, 0.0, 7.0), vec3(9.0, 12.0, 9.0), vec4(0.0, 4.0, 2.0, 16.0), 0, vec4(7.0, 7.0, 9.0, 9.0), 0, vec4(0.0, 4.0, 2.0, 16.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1;
}
// from minecraft:block/spore_blossom
bool block_40(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(1.0, 15.9, 1.0), vec3(15.0, 15.9, 15.0), vec4(1.0, 0.09999999999999964, 15.0, 0.09999999999999964), 0, vec4(1.0, 1.0, 15.0, 15.0), 0, vec4(1.0, 0.09999999999999964, 15.0, 0.09999999999999964), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(8.0, 15.7, 0.0), vec3(24.0, 15.7, 16.0), vec4(0.0, 0.3000000000000007, 16.0, 0.3000000000000007), 0, vec4(0.0, 0.0, 16.0, 16.0), 90, vec4(-8.0, 0.3000000000000007, 8.0, 0.3000000000000007), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube2 = cuboid(faces, rd, ro, vec3(-8.0, 15.7, 0.0), vec3(8.0, 15.7, 16.0), vec4(0.0, 0.3000000000000007, 16.0, 0.3000000000000007), 0, vec4(0.0, 0.0, 16.0, 16.0), 270, vec4(8.0, 0.3000000000000007, 24.0, 0.3000000000000007), 0, uvRange, t);
    if (cube2 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube3 = cuboid(faces, rd, ro, vec3(0.0, 15.7, 8.0), vec3(16.0, 15.7, 24.0), vec4(-8.0, 0.3000000000000007, 8.0, 0.3000000000000007), 0, vec4(16.0, 16.0, 0.0, 0.0), 0, vec4(0.0, 0.3000000000000007, 16.0, 0.3000000000000007), 0, uvRange, t);
    if (cube3 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube4 = cuboid(faces, rd, ro, vec3(0.0, 15.7, -8.0), vec3(16.0, 15.7, 8.0), vec4(8.0, 0.3000000000000007, 24.0, 0.3000000000000007), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 0.3000000000000007, 16.0, 0.3000000000000007), 0, uvRange, t);
    if (cube4 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1 || cube2 || cube3 || cube4;
}
// from minecraft:block/template_orientable_trapdoor_bottom
bool block_41(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 3.0, 16.0), vec4(0.0, 0.0, 16.0, 3.0), 0, vec4(0.0, 16.0, 16.0, 0.0), 0, vec4(0.0, 0.0, 16.0, 3.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0;
}
// from minecraft:block/mangrove_roots
bool block_42(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 8.0), vec3(16.0, 16.0, 8.0), vec4(8.0, 0.0, 8.0, 16.0), 0, vec4(0.0, 8.0, 16.0, 8.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(8.0, 0.0, 0.0), vec3(8.0, 16.0, 16.0), vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(8.0, 0.0, 8.0, 16.0), 0, vec4(8.0, 0.0, 8.0, 16.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube2 = cuboid(faces, rd, ro, vec3(0.0, 15.998, 0.0), vec3(16.0, 16.0, 16.0), vec4(0.0, 0.0, 16.0, 0.002000000000000668), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 0.002000000000000668), 0, uvRange, t);
    if (cube2 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube3 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 0.002, 16.0), vec4(0.0, 15.998, 16.0, 16.0), 0, vec4(0.0, 16.0, 16.0, 0.0), 0, vec4(0.0, 15.998, 16.0, 16.0), 0, uvRange, t);
    if (cube3 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube4 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 16.0, 0.002), vec4(15.998, 0.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 0.002), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, uvRange, t);
    if (cube4 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube5 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 15.998), vec3(16.0, 16.0, 16.0), vec4(0.0, 0.0, 0.002000000000000668, 16.0), 0, vec4(0.0, 15.998, 16.0, 16.0), 0, vec4(16.0, 0.0, 0.0, 16.0), 0, uvRange, t);
    if (cube5 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube6 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(0.002, 16.0, 16.0), vec4(16.0, 0.0, 0.0, 16.0), 0, vec4(0.0, 0.0, 0.002, 16.0), 0, vec4(15.998, 0.0, 16.0, 16.0), 0, uvRange, t);
    if (cube6 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube7 = cuboid(faces, rd, ro, vec3(15.998, 0.0, 0.0), vec3(16.0, 16.0, 16.0), vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(15.998, 0.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 0.002000000000000668, 16.0), 0, uvRange, t);
    if (cube7 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1 || cube2 || cube3 || cube4 || cube5 || cube6 || cube7;
}
// from minecraft:block/template_fence_gate
bool block_43(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 5.0, 7.0), vec3(2.0, 16.0, 9.0), vec4(7.0, 0.0, 9.0, 11.0), 0, vec4(0.0, 7.0, 2.0, 9.0), 0, vec4(0.0, 0.0, 2.0, 11.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(14.0, 5.0, 7.0), vec3(16.0, 16.0, 9.0), vec4(7.0, 0.0, 9.0, 11.0), 0, vec4(14.0, 7.0, 16.0, 9.0), 0, vec4(14.0, 0.0, 16.0, 11.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube2 = cuboid(faces, rd, ro, vec3(6.0, 6.0, 7.0), vec3(8.0, 15.0, 9.0), vec4(7.0, 1.0, 9.0, 10.0), 0, vec4(6.0, 7.0, 8.0, 9.0), 0, vec4(6.0, 1.0, 8.0, 10.0), 0, uvRange, t);
    if (cube2 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube3 = cuboid(faces, rd, ro, vec3(8.0, 6.0, 7.0), vec3(10.0, 15.0, 9.0), vec4(7.0, 1.0, 9.0, 10.0), 0, vec4(8.0, 7.0, 10.0, 9.0), 0, vec4(8.0, 1.0, 10.0, 10.0), 0, uvRange, t);
    if (cube3 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube4 = cuboid(faces, rd, ro, vec3(2.0, 6.0, 7.0), vec3(6.0, 9.0, 9.0), vec4(7.0, 7.0, 9.0, 10.0), 0, vec4(2.0, 7.0, 6.0, 9.0), 0, vec4(2.0, 7.0, 6.0, 10.0), 0, uvRange, t);
    if (cube4 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube5 = cuboid(faces, rd, ro, vec3(2.0, 12.0, 7.0), vec3(6.0, 15.0, 9.0), vec4(7.0, 1.0, 9.0, 4.0), 0, vec4(2.0, 7.0, 6.0, 9.0), 0, vec4(2.0, 1.0, 6.0, 4.0), 0, uvRange, t);
    if (cube5 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube6 = cuboid(faces, rd, ro, vec3(10.0, 6.0, 7.0), vec3(14.0, 9.0, 9.0), vec4(7.0, 7.0, 9.0, 10.0), 0, vec4(10.0, 7.0, 14.0, 9.0), 0, vec4(10.0, 7.0, 14.0, 10.0), 0, uvRange, t);
    if (cube6 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube7 = cuboid(faces, rd, ro, vec3(10.0, 12.0, 7.0), vec3(14.0, 15.0, 9.0), vec4(7.0, 1.0, 9.0, 4.0), 0, vec4(10.0, 7.0, 14.0, 9.0), 0, vec4(10.0, 1.0, 14.0, 4.0), 0, uvRange, t);
    if (cube7 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1 || cube2 || cube3 || cube4 || cube5 || cube6 || cube7;
}
// from minecraft:block/template_sculk_shrieker
bool block_44(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 8.0, 16.0), vec4(0.0, 8.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 8.0, 16.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(1.0, 8.0, 1.0), vec3(15.0, 15.0, 15.0), vec4(1.0, 1.0, 15.0, 8.0), 0, vec4(1.0, 1.0, 15.0, 15.0), 0, vec4(1.0, 1.0, 15.0, 8.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube2 = cuboid(faces, rd, ro, vec3(1.0, 14.98, 1.0), vec3(15.0, 14.98, 15.0), vec4(1.0, 1.0199999999999996, 15.0, 1.0199999999999996), 0, vec4(1.0, 1.0, 15.0, 15.0), 0, vec4(1.0, 1.0199999999999996, 15.0, 1.0199999999999996), 0, uvRange, t);
    if (cube2 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube3 = cuboid(faces, rd, ro, vec3(1.0, 8.0, 14.98), vec3(15.0, 15.0, 14.98), vec4(1.0199999999999996, 1.0, 1.0199999999999996, 8.0), 0, vec4(1.0, 14.98, 15.0, 14.98), 0, vec4(1.0, 1.0, 15.0, 8.0), 0, uvRange, t);
    if (cube3 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube4 = cuboid(faces, rd, ro, vec3(1.0, 8.0, 1.02), vec3(15.0, 15.0, 1.02), vec4(14.98, 1.0, 14.98, 8.0), 0, vec4(1.0, 1.02, 15.0, 1.02), 0, vec4(1.0, 1.0, 15.0, 8.0), 0, uvRange, t);
    if (cube4 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube5 = cuboid(faces, rd, ro, vec3(14.98, 8.0, 1.0), vec3(14.98, 15.0, 15.0), vec4(1.0, 1.0, 15.0, 8.0), 0, vec4(14.98, 1.0, 14.98, 15.0), 0, vec4(1.0199999999999996, 1.0, 1.0199999999999996, 8.0), 0, uvRange, t);
    if (cube5 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube6 = cuboid(faces, rd, ro, vec3(1.02, 8.0, 1.0), vec3(1.02, 15.0, 15.0), vec4(1.0, 1.0, 15.0, 8.0), 0, vec4(1.02, 1.0, 1.02, 15.0), 0, vec4(14.98, 1.0, 14.98, 8.0), 0, uvRange, t);
    if (cube6 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1 || cube2 || cube3 || cube4 || cube5 || cube6;
}
// from minecraft:block/small_dripleaf_top
bool block_45(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(8.0, 2.99, 8.0), vec3(15.0, 2.99, 15.0), vec4(1.0, 13.01, 8.0, 13.01), 0, vec4(8.0, 8.0, 0.0, 0.0), 0, vec4(1.0, 13.01, 8.0, 13.01), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube1 = cuboid(faces, rd, ro, vec3(1.0, 8.0, 1.0), vec3(8.0, 8.0, 8.0), vec4(8.0, 8.0, 15.0, 8.0), 0, vec4(0.0, 0.0, 8.0, 8.0), 0, vec4(8.0, 8.0, 15.0, 8.0), 0, uvRange, t);
    if (cube1 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube2 = cuboid(faces, rd, ro, vec3(1.0, 12.0, 8.0), vec3(8.0, 12.0, 15.0), vec4(1.0, 4.0, 8.0, 4.0), 0, vec4(0.0, 0.0, 8.0, 8.0), 270, vec4(8.0, 4.0, 15.0, 4.0), 0, uvRange, t);
    if (cube2 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube3 = cuboid(faces, rd, ro, vec3(8.0, 2.0, 8.0), vec3(15.0, 3.0, 15.0), vec4(0.0, 0.0, 8.0, 1.0), 0, vec4(8.0, 8.0, 15.0, 15.0), 0, vec4(0.0, 0.0, 8.0, 1.0), 0, uvRange, t);
    if (cube3 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube4 = cuboid(faces, rd, ro, vec3(1.0, 7.0, 1.01), vec3(8.0, 8.0, 8.0), vec4(0.0, 0.0, 8.0, 1.0), 0, vec4(1.0, 1.01, 8.0, 8.0), 0, vec4(0.0, 0.0, 8.0, 1.0), 0, uvRange, t);
    if (cube4 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube5 = cuboid(faces, rd, ro, vec3(1.0, 11.0, 8.0), vec3(8.0, 12.0, 15.0), vec4(0.0, 0.0, 8.0, 1.0), 0, vec4(1.0, 8.0, 8.0, 15.0), 0, vec4(0.0, 0.0, 8.0, 1.0), 0, uvRange, t);
    if (cube5 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube6 = cuboid(faces, rd, ro, vec3(4.5, 0.0, 8.0), vec3(11.5, 14.0, 8.0), vec4(8.0, 2.0, 8.0, 16.0), 0, vec4(4.5, 8.0, 11.5, 8.0), 0, vec4(4.0, 0.0, 12.0, 14.0), 0, uvRange, t);
    if (cube6 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    bool cube7 = cuboid(faces, rd, ro, vec3(4.5, 0.0, 8.0), vec3(11.5, 14.0, 8.0), vec4(8.0, 2.0, 8.0, 16.0), 0, vec4(4.5, 8.0, 11.5, 8.0), 0, vec4(4.0, 0.0, 12.0, 14.0), 0, uvRange, t);
    if (cube7 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0 || cube1 || cube2 || cube3 || cube4 || cube5 || cube6 || cube7;
}
// from minecraft:block/dried_kelp_block
bool block_46(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 16.0, 16.0), vec4(16.0, 0.0, 0.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0;
}
// from minecraft:block/enchanting_table
bool block_47(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 12.0, 16.0), vec4(0.0, 4.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 4.0, 16.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0;
}
// from minecraft:block/end_portal_frame
bool block_48(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 13.0, 16.0), vec4(0.0, 3.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 3.0, 16.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0;
}
// from minecraft:block/template_daylight_detector
bool block_49(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 6.0, 16.0), vec4(0.0, 10.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 10.0, 16.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0;
}
// from minecraft:block/pressure_plate_up
bool block_50(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(1.0, 0.0, 1.0), vec3(15.0, 1.0, 15.0), vec4(1.0, 15.0, 15.0, 16.0), 0, vec4(1.0, 1.0, 15.0, 15.0), 0, vec4(1.0, 15.0, 15.0, 16.0), 0, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0;
}
// from minecraft:block/template_glazed_terracotta
bool block_51(int faces, vec3 rd, vec3 ro) {
    vec4 uvRange = getUV();
    float minT = 99999999;
    float t;
    vec4 postCol;
    bool cube0 = cuboid(faces, rd, ro, vec3(0.0, 0.0, 0.0), vec3(16.0, 16.0, 16.0), vec4(0.0, 0.0, 16.0, 16.0), 180, vec4(0.0, 0.0, 16.0, 16.0), 0, vec4(0.0, 0.0, 16.0, 16.0), 90, uvRange, t);
    if (cube0 && t < minT) {
        minT = t;
        postCol = fragColor;
    }
    fragColor = postCol;
    return cube0;
}
bool custom_block(int modelID, int faces, vec3 rd, vec3 ro) {
    switch (modelID) {
        case 1:
            return block_1(faces, rd, ro);
        case 2:
            return block_2(faces, rd, ro);
        case 3:
            return block_3(faces, rd, ro);
        case 4:
            return block_4(faces, rd, ro);
        case 5:
            return block_5(faces, rd, ro);
        case 6:
            return block_6(faces, rd, ro);
        case 7:
            return block_7(faces, rd, ro);
        case 8:
            return block_8(faces, rd, ro);
        case 9:
            return block_9(faces, rd, ro);
        case 10:
            return block_10(faces, rd, ro);
        case 11:
            return block_11(faces, rd, ro);
        case 12:
            return block_12(faces, rd, ro);
        case 13:
            return block_13(faces, rd, ro);
        case 14:
            return block_14(faces, rd, ro);
        case 15:
            return block_15(faces, rd, ro);
        case 16:
            return block_16(faces, rd, ro);
        case 17:
            return block_17(faces, rd, ro);
        case 18:
            return block_18(faces, rd, ro);
        case 19:
            return block_19(faces, rd, ro);
        case 20:
            return block_20(faces, rd, ro);
        case 21:
            return block_21(faces, rd, ro);
        case 22:
            return block_22(faces, rd, ro);
        case 23:
            return block_23(faces, rd, ro);
        case 24:
            return block_24(faces, rd, ro);
        case 25:
            return block_25(faces, rd, ro);
        case 26:
            return block_26(faces, rd, ro);
        case 27:
            return block_27(faces, rd, ro);
        case 28:
            return block_28(faces, rd, ro);
        case 29:
            return block_29(faces, rd, ro);
        case 30:
            return block_30(faces, rd, ro);
        case 31:
            return block_31(faces, rd, ro);
        case 32:
            return block_32(faces, rd, ro);
        case 33:
            return block_33(faces, rd, ro);
        case 34:
            return block_34(faces, rd, ro);
        case 35:
            return block_35(faces, rd, ro);
        case 36:
            return block_36(faces, rd, ro);
        case 37:
            return block_37(faces, rd, ro);
        case 38:
            return block_38(faces, rd, ro);
        case 39:
            return block_39(faces, rd, ro);
        case 40:
            return block_40(faces, rd, ro);
        case 41:
            return block_41(faces, rd, ro);
        case 42:
            return block_42(faces, rd, ro);
        case 43:
            return block_43(faces, rd, ro);
        case 44:
            return block_44(faces, rd, ro);
        case 45:
            return block_45(faces, rd, ro);
        case 46:
            return block_46(faces, rd, ro);
        case 47:
            return block_47(faces, rd, ro);
        case 48:
            return block_48(faces, rd, ro);
        case 49:
            return block_49(faces, rd, ro);
        case 50:
            return block_50(faces, rd, ro);
        case 51:
            return block_51(faces, rd, ro);
    }
    return false;
}
// custom blocks end

void main() {
    if (modelID != -1) {
        // Get ray properties (ray direction, ray origin)
        vec3 rd = normalize(vec3(-0.6123, -0.5, -0.6123));
        vec3 localX = normalize(cross(vec3(0.0, 1.0, 0.0), rd));
        vec3 localY = normalize(cross(rd, localX));
        vec3 ro = (-localX * screenPos.x + localY * screenPos.y);
        if (custom_block(modelID, faces, rd, ro)) return;
        else discard;
    }
    vec4 color = texture(Sampler0, texCoord0) * vertexColor * ColorModulator;
    if (color.a < 0.1) {
        discard;
    }
    fragColor = linear_fog(color, vertexDistance, FogStart, FogEnd, FogColor);
}
