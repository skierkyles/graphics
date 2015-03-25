var image = document.querySelector('#drawing');
var width = 500 * 0.5;
var height = 500 * 0.5;

image.width = width;
image.height = height;

image.style.cssText = 'width:' + (width * 2) + 'px;height:' + (height * 2) + 'px';

var ctx = image.getContext('2d');
var data = ctx.getImageData(0, 0, width, height);

var scene = {};

// Camera
scene.camera = {
  point: {
    x: 0,
    y: -1.2,
    z: 12
  },
  fieldOfView: 45,
  vector: {
    x: 0,
    y: 0,
    z: 0
  }
};


// Lights
scene.lights = [
  {
    x: 0,
    y: 10,
    z: 0
  },
];

// Objects
scene.objects = [
  {
    type: 'sphere',
    point: {
      x: 0,
      y: 0,
      z: 3
    },
    color: {
      r: 255,
      g: 127,
      b: 127
    },
    specular: 0.1,
    lambert: 0.9,
    ambient: 0.0,
    radius: 1
  },
  //////
  {
    type: 'sphere',
    point: {
      x: 2,
      y: 0,
      z: -4
    },
    color: {
      r: 127,
      g: 255,
      b: 127
    },
    specular: 0.1,
    lambert: 0.9,
    ambient: 0.0,
    radius: 1
  },
  ///////
  {
    type: 'sphere',
    point: {
      x: -2,
      y: 0,
      z: -3
    },
    color: {
      r: 127,
      g: 127,
      b: 255
    },
    specular: 0.1,
    lambert: 0.9,
    ambient: 0.1,
    radius: 1
  },
  ///////
  {
    type: 'sphere',
    point: {
      x: 0,
      y: 100,
      z: 0
    },
    color: {
      r: 255,
      g: 255,
      b: 255
    },
    specular: 0.1,
    lambert: 0.9,
    ambient: 0.1,
    radius: 98.5
  }
]

function render(scene) {
  var camera = scene.camera;
  var objects = scene.objects;
  var lights = scene.lights;

  console.log(camera);

  var eyeVector = Vector.unitVector(Vector.subtract(camera.vector, camera.point)),
      viewPointRight = Vector.unitVector(Vector.crossProduct(eyeVector, Vector.UP)),
      viewPointUp = Vector.unitVector(Vector.crossProduct(viewPointRight, eyeVector)),

      fovRadians = Math.PI * (camera.fieldOfView / 2) / 180,
      heightWidthRatio = height / width,
      halfWidth = Math.tan(fovRadians),
      halfHeight = heightWidthRatio * halfWidth,
      cameraWidth = halfWidth * 2,
      cameraHeight = halfHeight * 2,
      pixelWidth = cameraWidth / (width - 1),
      pixelHeight = cameraHeight / (height - 1);

  var index, color;
  var ray = {
    point: camera.point,
  };

  for (var x = 0; x < width; x++) {
    for (var y = 0; y < height; y++) {
      var xComponent = Vector.scale(viewPointRight, (x * pixelWidth) - halfWidth),
          yComponent = Vector.scale(viewPointUp, (y * pixelHeight) - halfHeight);

      ray.vector = Vector.unitVector(Vector.add3(eyeVector, xComponent, yComponent));

      color = trace(ray, scene);
      index = (x * 4) + (y * width * 4);

      data.data[index + 0] = color.r;
      data.data[index + 1] = color.g;
      data.data[index + 2] = color.b;
      data.data[index + 3] = 255;
    }
  }

  console.log("Rendered the Image");
  console.log(data);
  ctx.putImageData(data, 0, 0);
}

function trace(ray, scene, depth) {
  if (depth === undefined) {
    depth = 0;
  }

  if (depth > 3) return;

  var distance_and_object = intersectScene(ray, scene);
  var distance = distance_and_object.distance;
  var object = distance_and_object.object;


  if (distance === Infinity) {
    return {
      // TODO set the proper bg.
      r: 0,
      g: 51*(1 - ray.vector.y),
      b: 25.5
    }
  } else {
    var intersection_point = Vector.add(ray.point, Vector.scale(ray.vector, distance));

    return surface(ray, scene, object, intersection_point, sphereNormal(object, intersection_point), depth);
  }
}

function intersectScene(ray, scene) {
  var closest = {
    distance: Infinity,
    object: null
  };

  for (var i = 0; i < scene.objects.length; i++) {
    var object = scene.objects[i],
        dist = sphereIntersection(object, ray);

    var closer = dist < closest.distance;

    if (dist !== undefined && closer) {
      closest.distance = dist;
      closest.object = object;
    }
  }

  return closest;
}

function sphereIntersection(sphere, ray) {
  var eye_to_center = Vector.subtract(sphere.point, ray.point),
      vector_side = Vector.dotProduct(eye_to_center, ray.vector),
      camera_to_center = Vector.dotProduct(eye_to_center, eye_to_center),
      discriminant = (sphere.radius * sphere.radius) - camera_to_center + (vector_side * vector_side);

  if (discriminant < 0) {
    // The ray didn't hit this sphere.
    return;
  } else {
    return vector_side - Math.sqrt(discriminant);
  }
}

function sphereNormal(sphere, pos) {
  return Vector.unitVector(Vector.subtract(pos, sphere.point));
}

function surface(ray, scene, object, intersection_point, normal, depth) {
  var base = object.color;
  var lambertAmount = 0;

  if (object.lambert) {
    for (var i = 0; i < scene.lights.length; i++) {
      var lightPoint = scene.lights[i];

      if (!isLightVisible(intersection_point, scene, lightPoint)) {
        var contrib = Vector.dotProduct(Vector.unitVector(
          Vector.subtract(lightPoint, intersection_point)), normal);

        if (contrib > 0) lambertAmount += contrib;
      };
    }
  }

  lambertAmount = Math.min(1, lambertAmount);

  var tmp = Vector.add3(Vector.ZERO,
          Vector.scale(base, lambertAmount * object.lambert),
          Vector.scale(base, object.ambient));

  return {
    r: tmp.x,
    g: tmp.y,
    b: tmp.z
  }
}

function isLightVisible(pt, scene, light) {
  var distance_and_object = intersectScene({
                      point: pt,
                      vector: Vector.unitVector(Vector.subtract(pt, light))
                    },
                    scene);
  return distance_and_object.distance > -0.005;
}




render(scene);
