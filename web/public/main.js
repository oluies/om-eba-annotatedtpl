'use strict';
import * as $i_https$003a$002f$002fcdn$002ejsdelivr$002enet$002fnpm$002f$0040duckdb$002fduckdb$002dwasm$00401$002e29$002e0$002f$002besm from "https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.29.0/+esm";
var $p;
var $fileLevelThis = this;
var $getOwnPropertyDescriptors = (Object.getOwnPropertyDescriptors || (() => {
  var ownKeysFun;
  if ((((typeof Reflect) !== "undefined") && Reflect.ownKeys)) {
    ownKeysFun = Reflect.ownKeys;
  } else {
    var getOwnPropertySymbols = (Object.getOwnPropertySymbols || ((o) => []));
    ownKeysFun = ((o) => Object.getOwnPropertyNames(o).concat(getOwnPropertySymbols(o)));
  }
  return ((o) => {
    var ownKeys = ownKeysFun(o);
    var descriptors = ({});
    var len = (ownKeys.length | 0);
    var i = 0;
    while ((i !== len)) {
      var key = ownKeys[i];
      Object.defineProperty(descriptors, key, ({
        "configurable": true,
        "enumerable": true,
        "writable": true,
        "value": Object.getOwnPropertyDescriptor(o, key)
      }));
      i = ((i + 1) | 0);
    }
    return descriptors;
  });
})());
function $Char(c) {
  this.c = c;
}
$p = $Char.prototype;
$p.toString = (function() {
  return String.fromCharCode(this.c);
});
function $Long(lo, hi) {
  this.l = lo;
  this.h = hi;
}
$p = $Long.prototype;
$p.toString = (function() {
  return $s_RTLong__toString__I__I__T(this.l, this.h);
});
function $noIsInstance(arg0) {
  throw new TypeError("Cannot call isInstance() on a Class representing a JS trait/object");
}
function $objectClone(arg0) {
  return Object.create(Object.getPrototypeOf(arg0), $getOwnPropertyDescriptors(arg0));
}
function $objectOrArrayClone(arg0) {
  return (arg0.$classData.Z ? arg0.e() : $objectClone(arg0));
}
function $objectGetClass(arg0) {
  switch ((typeof arg0)) {
    case "string": {
      return $d_T.l();
    }
    case "number": {
      if ($isInt(arg0)) {
        if ((((arg0 << 24) >> 24) === arg0)) {
          return $d_jl_Byte.l();
        } else if ((((arg0 << 16) >> 16) === arg0)) {
          return $d_jl_Short.l();
        } else {
          return $d_jl_Integer.l();
        }
      } else if ($isFloat(arg0)) {
        return $d_jl_Float.l();
      } else {
        return $d_jl_Double.l();
      }
    }
    case "boolean": {
      return $d_jl_Boolean.l();
    }
    case "undefined": {
      return $d_jl_Void.l();
    }
    default: {
      if ((arg0 instanceof $Long)) {
        return $d_jl_Long.l();
      } else if ((arg0 instanceof $Char)) {
        return $d_jl_Character.l();
      } else if ((!(!(arg0 && arg0.$classData)))) {
        return arg0.$classData.l();
      } else {
        return null;
      }
    }
  }
}
function $objectClassName(arg0) {
  switch ((typeof arg0)) {
    case "string": {
      return "java.lang.String";
    }
    case "number": {
      if ($isInt(arg0)) {
        if ((((arg0 << 24) >> 24) === arg0)) {
          return "java.lang.Byte";
        } else if ((((arg0 << 16) >> 16) === arg0)) {
          return "java.lang.Short";
        } else {
          return "java.lang.Integer";
        }
      } else if ($isFloat(arg0)) {
        return "java.lang.Float";
      } else {
        return "java.lang.Double";
      }
    }
    case "boolean": {
      return "java.lang.Boolean";
    }
    case "undefined": {
      return "java.lang.Void";
    }
    default: {
      if ((arg0 instanceof $Long)) {
        return "java.lang.Long";
      } else if ((arg0 instanceof $Char)) {
        return "java.lang.Character";
      } else if ((!(!(arg0 && arg0.$classData)))) {
        return arg0.$classData.N;
      } else {
        return null.rP();
      }
    }
  }
}
function $dp_equals__O__Z(instance, x0) {
  switch ((typeof instance)) {
    case "string": {
      return $f_T__equals__O__Z(instance, x0);
    }
    case "number": {
      return $f_jl_Double__equals__O__Z(instance, x0);
    }
    case "boolean": {
      return $f_jl_Boolean__equals__O__Z(instance, x0);
    }
    case "undefined": {
      return $f_jl_Void__equals__O__Z(instance, x0);
    }
    default: {
      if (((!(!(instance && instance.$classData))) || (instance === null))) {
        return instance.k(x0);
      } else if ((instance instanceof $Long)) {
        return $f_jl_Long__equals__O__Z(instance.l, instance.h, x0);
      } else if ((instance instanceof $Char)) {
        return $f_jl_Character__equals__O__Z(instance.c, x0);
      } else {
        return $c_O.prototype.k.call(instance, x0);
      }
    }
  }
}
function $dp_hashCode__I(instance) {
  switch ((typeof instance)) {
    case "string": {
      return $f_T__hashCode__I(instance);
    }
    case "number": {
      return $f_jl_Double__hashCode__I(instance);
    }
    case "boolean": {
      return $f_jl_Boolean__hashCode__I(instance);
    }
    case "undefined": {
      return $f_jl_Void__hashCode__I(instance);
    }
    default: {
      if (((!(!(instance && instance.$classData))) || (instance === null))) {
        return instance.r();
      } else if ((instance instanceof $Long)) {
        return $f_jl_Long__hashCode__I(instance.l, instance.h);
      } else if ((instance instanceof $Char)) {
        return $f_jl_Character__hashCode__I(instance.c);
      } else {
        return $c_O.prototype.r.call(instance);
      }
    }
  }
}
function $dp_indexOf__I__I(instance, x0) {
  if (((typeof instance) === "string")) {
    return $f_T__indexOf__I__I(instance, x0);
  } else {
    return instance.rQ(x0);
  }
}
function $dp_toString__T(instance) {
  return ((instance === (void 0)) ? "undefined" : instance.toString());
}
function $dp_trim__T(instance) {
  if (((typeof instance) === "string")) {
    return $f_T__trim__T(instance);
  } else {
    return instance.rV();
  }
}
function $checkIntDivisor(arg0) {
  if ((arg0 === 0)) {
    throw new $c_jl_ArithmeticException("/ by zero");
  } else {
    return arg0;
  }
}
function $doubleToInt(arg0) {
  return ((arg0 > 2147483647) ? 2147483647 : ((arg0 < (-2147483648)) ? (-2147483648) : (arg0 | 0)));
}
function $cToS(arg0) {
  return String.fromCharCode(arg0);
}
var $fpBitsDataView = new DataView(new ArrayBuffer(8));
function $floatToBits(arg0) {
  var dataView = $fpBitsDataView;
  dataView.setFloat32(0, arg0, true);
  return dataView.getInt32(0, true);
}
function $floatFromBits(arg0) {
  var dataView = $fpBitsDataView;
  dataView.setInt32(0, arg0, true);
  return dataView.getFloat32(0, true);
}
function $doubleToBits(arg0) {
  var dataView = $fpBitsDataView;
  return $s_RTLong__fromDoubleBits__D__O__J(arg0, dataView);
}
function $doubleFromBits(arg0) {
  var dataView = $fpBitsDataView;
  return $s_RTLong__bitsToDouble__I__I__O__D(arg0.l, arg0.h, dataView);
}
function $resolveSuperRef(arg0, arg1) {
  var getPrototypeOf = Object.getPrototyeOf;
  var getOwnPropertyDescriptor = Object.getOwnPropertyDescriptor;
  var superProto = arg0.prototype;
  while ((superProto !== null)) {
    var desc = getOwnPropertyDescriptor(superProto, arg1);
    if ((desc !== (void 0))) {
      return desc;
    }
    superProto = getPrototypeOf(superProto);
  }
}
function $superGet(arg0, arg1, arg2) {
  var desc = $resolveSuperRef(arg0, arg2);
  if ((desc !== (void 0))) {
    var getter = desc.get;
    return ((getter !== (void 0)) ? getter.call(arg1) : getter.value);
  }
}
function $superSet(arg0, arg1, arg2, arg3) {
  var desc = $resolveSuperRef(arg0, arg2);
  if ((desc !== (void 0))) {
    var setter = desc.set;
    if ((setter !== (void 0))) {
      setter.call(arg1, arg3);
      return (void 0);
    }
  }
  throw new TypeError((("super has no setter '" + arg2) + "'."));
}
function $arraycopyGeneric(arg0, arg1, arg2, arg3, arg4) {
  if (((arg0 !== arg2) || (((arg3 - arg1) >>> 0) > (arg4 >>> 0)))) {
    for (var i = 0; (i < arg4); i = ((i + 1) | 0)) {
      arg2[((arg3 + i) | 0)] = arg0[((arg1 + i) | 0)];
    }
  } else {
    for (var i = ((arg4 - 1) | 0); (i >= 0); i = ((i - 1) | 0)) {
      arg2[((arg3 + i) | 0)] = arg0[((arg1 + i) | 0)];
    }
  }
}
var $lastIDHash = 0;
var $idHashCodeMap = new WeakMap();
function $systemIdentityHashCode(obj) {
  switch ((typeof obj)) {
    case "string": {
      return $f_T__hashCode__I(obj);
    }
    case "number": {
      return $f_jl_Double__hashCode__I(obj);
    }
    case "bigint": {
      var biHash = 0;
      if ((obj < BigInt(0))) {
        obj = (~obj);
      }
      while ((obj !== BigInt(0))) {
        biHash = (biHash ^ Number(BigInt.asIntN(32, obj)));
        obj = (obj >> BigInt(32));
      }
      return biHash;
    }
    case "boolean": {
      return (obj ? 1231 : 1237);
    }
    case "undefined": {
      return 0;
    }
    case "symbol": {
      var description = obj.description;
      return ((description === (void 0)) ? 0 : $f_T__hashCode__I(description));
    }
    default: {
      if ((obj === null)) {
        return 0;
      } else {
        var hash = $idHashCodeMap.get(obj);
        if ((hash === (void 0))) {
          hash = (($lastIDHash + 1) | 0);
          $lastIDHash = hash;
          $idHashCodeMap.set(obj, hash);
        }
        return hash;
      }
    }
  }
}
function $isByte(arg0) {
  return ((((typeof arg0) === "number") && (((arg0 << 24) >> 24) === arg0)) && ((1 / arg0) !== (1 / (-0))));
}
function $isShort(arg0) {
  return ((((typeof arg0) === "number") && (((arg0 << 16) >> 16) === arg0)) && ((1 / arg0) !== (1 / (-0))));
}
function $isInt(arg0) {
  return ((((typeof arg0) === "number") && ((arg0 | 0) === arg0)) && ((1 / arg0) !== (1 / (-0))));
}
function $isFloat(arg0) {
  return (((typeof arg0) === "number") && ((arg0 !== arg0) || (Math.fround(arg0) === arg0)));
}
function $bC(arg0) {
  return new $Char(arg0);
}
var $bC0 = $bC(0);
function $bL(arg0, arg1) {
  return new $Long(arg0, arg1);
}
var $bL0 = $bL(0, 0);
function $uC(arg0) {
  return ((arg0 === null) ? 0 : arg0.c);
}
function $uJ(arg0) {
  return ((arg0 === null) ? $bL0 : arg0);
}
function $ct_O__($thiz) {
  return $thiz;
}
/** @constructor */
function $c_O() {
}
$p = $c_O.prototype;
$p.constructor = $c_O;
/** @constructor */
function $h_O() {
}
$h_O.prototype = $p;
$p.r = (function() {
  return $systemIdentityHashCode(this);
});
$p.k = (function(that) {
  return (this === that);
});
$p.t = (function() {
  var i = this.r();
  return (($objectClassName(this) + "@") + (i >>> 0.0).toString(16));
});
$p.toString = (function() {
  return this.t();
});
function $ac_O(arg) {
  if (((typeof arg) === "number")) {
    this.a = new Array(arg);
    for (var i = 0; (i < arg); (i++)) {
      this.a[i] = null;
    }
  } else {
    this.a = arg;
  }
}
$p = $ac_O.prototype = new $h_O();
$p.constructor = $ac_O;
$p.u = (function(srcPos, dest, destPos, length) {
  $arraycopyGeneric(this.a, srcPos, dest.a, destPos, length);
});
$p.e = (function() {
  return new $ac_O(this.a.slice());
});
function $ah_O() {
}
$ah_O.prototype = $p;
function $ac_Z(arg) {
  if (((typeof arg) === "number")) {
    this.a = new Array(arg);
    for (var i = 0; (i < arg); (i++)) {
      this.a[i] = false;
    }
  } else {
    this.a = arg;
  }
}
$p = $ac_Z.prototype = new $h_O();
$p.constructor = $ac_Z;
$p.u = (function(srcPos, dest, destPos, length) {
  $arraycopyGeneric(this.a, srcPos, dest.a, destPos, length);
});
$p.e = (function() {
  return new $ac_Z(this.a.slice());
});
function $ac_C(arg) {
  if (((typeof arg) === "number")) {
    this.a = new Uint16Array(arg);
  } else {
    this.a = arg;
  }
}
$p = $ac_C.prototype = new $h_O();
$p.constructor = $ac_C;
$p.u = (function(srcPos, dest, destPos, length) {
  dest.a.set(this.a.subarray(srcPos, ((srcPos + length) | 0)), destPos);
});
$p.e = (function() {
  return new $ac_C(this.a.slice());
});
function $ac_B(arg) {
  if (((typeof arg) === "number")) {
    this.a = new Int8Array(arg);
  } else {
    this.a = arg;
  }
}
$p = $ac_B.prototype = new $h_O();
$p.constructor = $ac_B;
$p.u = (function(srcPos, dest, destPos, length) {
  dest.a.set(this.a.subarray(srcPos, ((srcPos + length) | 0)), destPos);
});
$p.e = (function() {
  return new $ac_B(this.a.slice());
});
function $ac_S(arg) {
  if (((typeof arg) === "number")) {
    this.a = new Int16Array(arg);
  } else {
    this.a = arg;
  }
}
$p = $ac_S.prototype = new $h_O();
$p.constructor = $ac_S;
$p.u = (function(srcPos, dest, destPos, length) {
  dest.a.set(this.a.subarray(srcPos, ((srcPos + length) | 0)), destPos);
});
$p.e = (function() {
  return new $ac_S(this.a.slice());
});
function $ac_I(arg) {
  if (((typeof arg) === "number")) {
    this.a = new Int32Array(arg);
  } else {
    this.a = arg;
  }
}
$p = $ac_I.prototype = new $h_O();
$p.constructor = $ac_I;
$p.u = (function(srcPos, dest, destPos, length) {
  dest.a.set(this.a.subarray(srcPos, ((srcPos + length) | 0)), destPos);
});
$p.e = (function() {
  return new $ac_I(this.a.slice());
});
function $ac_J(arg) {
  if (((typeof arg) === "number")) {
    arg = (arg << 1);
    this.a = new Int32Array(arg);
  } else {
    this.a = arg;
  }
}
$p = $ac_J.prototype = new $h_O();
$p.constructor = $ac_J;
$p.u = (function(srcPos, dest, destPos, length) {
  dest.a.set(this.a.subarray((srcPos << 1), (((srcPos + length) | 0) << 1)), (destPos << 1));
});
$p.e = (function() {
  return new $ac_J(this.a.slice());
});
function $ac_F(arg) {
  if (((typeof arg) === "number")) {
    this.a = new Float32Array(arg);
  } else {
    this.a = arg;
  }
}
$p = $ac_F.prototype = new $h_O();
$p.constructor = $ac_F;
$p.u = (function(srcPos, dest, destPos, length) {
  dest.a.set(this.a.subarray(srcPos, ((srcPos + length) | 0)), destPos);
});
$p.e = (function() {
  return new $ac_F(this.a.slice());
});
function $ac_D(arg) {
  if (((typeof arg) === "number")) {
    this.a = new Float64Array(arg);
  } else {
    this.a = arg;
  }
}
$p = $ac_D.prototype = new $h_O();
$p.constructor = $ac_D;
$p.u = (function(srcPos, dest, destPos, length) {
  dest.a.set(this.a.subarray(srcPos, ((srcPos + length) | 0)), destPos);
});
$p.e = (function() {
  return new $ac_D(this.a.slice());
});
function $TypeData() {
  this.C = (void 0);
  this.n = null;
  this.O = null;
  this.B = null;
  this.D = 0;
  this.z = null;
  this.E = "";
  this.L = (void 0);
  this.A = (void 0);
  this.F = (void 0);
  this.w = (void 0);
  this.J = false;
  this.N = "";
  this.X = false;
  this.Y = false;
  this.Z = false;
  this.I = (void 0);
}
$p = $TypeData.prototype;
$p.p = (function(zero, arrayEncodedName, displayName, arrayClass, typedArrayClass) {
  this.n = ({});
  this.z = zero;
  this.E = arrayEncodedName;
  var self = this;
  this.F = ((that) => (that === self));
  this.N = displayName;
  this.X = true;
  this.I = ((obj) => false);
  if ((arrayClass !== (void 0))) {
    this.A = new $TypeData().y(this, arrayClass, typedArrayClass, (arrayEncodedName === "J"));
  }
  return this;
});
$p.i = (function(kindOrCtor, fullName, ancestors, isInstance) {
  var internalName = Object.getOwnPropertyNames(ancestors)[0];
  this.n = ancestors;
  this.E = (("L" + fullName) + ";");
  this.F = ((that) => (!(!that.n[internalName])));
  this.J = (kindOrCtor === 2);
  this.N = fullName;
  this.Y = (kindOrCtor === 1);
  this.I = (isInstance || ((obj) => (!(!((obj && obj.$classData) && obj.$classData.n[internalName])))));
  if (((typeof kindOrCtor) !== "number")) {
    kindOrCtor.prototype.$classData = this;
  }
  return this;
});
$p.y = (function(componentData, arrayClass, typedArrayClass, isLongArray, isAssignableFromFun) {
  arrayClass.prototype.$classData = this;
  var name = ("[" + componentData.E);
  this.C = arrayClass;
  this.n = ({
    A: 1,
    a: 1
  });
  this.O = componentData;
  this.B = componentData;
  this.D = 1;
  this.E = name;
  this.N = name;
  this.Z = true;
  var self = this;
  this.F = (isAssignableFromFun || ((that) => (self === that)));
  this.w = (isLongArray ? ((array) => {
    var len = (array.length | 0);
    var result = new arrayClass(len);
    var u = result.a;
    for (var i = 0; (i < len); i = ((i + 1) | 0)) {
      var srcElem = array[i];
      u[(i << 1)] = srcElem.l;
      u[(((i << 1) + 1) | 0)] = srcElem.h;
    }
    return result;
  }) : (typedArrayClass ? ((array) => new arrayClass(new typedArrayClass(array))) : ((array) => new arrayClass(array))));
  this.I = ((obj) => (obj instanceof arrayClass));
  return this;
});
$p.a = (function(componentData) {
  function ArrayClass(arg) {
    if (((typeof arg) === "number")) {
      this.a = new Array(arg);
      for (var i = 0; (i < arg); (i++)) {
        this.a[i] = null;
      }
    } else {
      this.a = arg;
    }
  }
  var $p = ArrayClass.prototype = new $ah_O();
  $p.constructor = ArrayClass;
  $p.u = (function(srcPos, dest, destPos, length) {
    $arraycopyGeneric(this.a, srcPos, dest.a, destPos, length);
  });
  $p.e = (function() {
    return new ArrayClass(this.a.slice());
  });
  $p.$classData = this;
  var arrayBase = (componentData.B || componentData);
  var arrayDepth = (componentData.D + 1);
  var name = ("[" + componentData.E);
  this.C = ArrayClass;
  this.n = ({
    A: 1,
    a: 1
  });
  this.O = componentData;
  this.B = arrayBase;
  this.D = arrayDepth;
  this.E = name;
  this.N = name;
  this.Z = true;
  var isAssignableFromFun = ((that) => {
    var thatDepth = that.D;
    return ((thatDepth === arrayDepth) ? arrayBase.F(that.B) : ((thatDepth > arrayDepth) && (arrayBase === $d_O)));
  });
  this.F = isAssignableFromFun;
  this.w = ((array) => new ArrayClass(array));
  var self = this;
  this.I = ((obj) => {
    var data = (obj && obj.$classData);
    return ((!(!data)) && ((data === self) || isAssignableFromFun(data)));
  });
  return this;
});
$p.r = (function() {
  if ((!this.A)) {
    this.A = new $TypeData().a(this);
  }
  return this.A;
});
$p.l = (function() {
  if ((!this.L)) {
    this.L = new $c_jl_Class(this);
  }
  return this.L;
});
$p.R = (function(that) {
  return ((this === that) || this.F(that));
});
$p.S = (function() {
  return (this.P ? this.P.l() : null);
});
$p.Q = (function() {
  return (this.O ? this.O.l() : null);
});
$p.U = (function(length) {
  if ((this === $d_V)) {
    throw $ct_jl_IllegalArgumentException__(new $c_jl_IllegalArgumentException());
  }
  return new (this.r().C)(length);
});
function $isArrayOf_O(obj, depth) {
  var data = (obj && obj.$classData);
  if ((!data)) {
    return false;
  } else {
    var arrayDepth = data.D;
    return ((arrayDepth === depth) ? (!data.B.X) : (arrayDepth > depth));
  }
}
function $isArrayOf_Z(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && (obj.$classData.B === $d_Z))));
}
function $isArrayOf_C(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && (obj.$classData.B === $d_C))));
}
function $isArrayOf_B(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && (obj.$classData.B === $d_B))));
}
function $isArrayOf_S(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && (obj.$classData.B === $d_S))));
}
function $isArrayOf_I(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && (obj.$classData.B === $d_I))));
}
function $isArrayOf_J(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && (obj.$classData.B === $d_J))));
}
function $isArrayOf_F(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && (obj.$classData.B === $d_F))));
}
function $isArrayOf_D(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && (obj.$classData.B === $d_D))));
}
var $d_O = new $TypeData();
$d_O.n = ({});
$d_O.E = "Ljava.lang.Object;";
$d_O.F = ((that) => (!that.X));
$d_O.N = "java.lang.Object";
$d_O.I = ((obj) => (obj !== null));
$d_O.A = new $TypeData().y($d_O, $ac_O, (void 0), false, ((that) => {
  var thatDepth = that.D;
  return ((thatDepth === 1) ? (!that.B.X) : (thatDepth > 1));
}));
$c_O.prototype.$classData = $d_O;
var $d_V = new $TypeData().p((void 0), "V", "void", (void 0), (void 0));
var $d_Z = new $TypeData().p(false, "Z", "boolean", $ac_Z, (void 0));
var $d_C = new $TypeData().p(0, "C", "char", $ac_C, Uint16Array);
var $d_B = new $TypeData().p(0, "B", "byte", $ac_B, Int8Array);
var $d_S = new $TypeData().p(0, "S", "short", $ac_S, Int16Array);
var $d_I = new $TypeData().p(0, "I", "int", $ac_I, Int32Array);
var $d_J = new $TypeData().p($bL0, "J", "long", $ac_J, Int32Array);
var $d_F = new $TypeData().p(0.0, "F", "float", $ac_F, Float32Array);
var $d_D = new $TypeData().p(0.0, "D", "double", $ac_D, Float64Array);
var $typedArraysAreBigEndian = (new Int8Array(new Int32Array([1]).buffer)[0] === 0);
function $constArrayBuffer_B(len, encoded) {
  var buf = new ArrayBuffer(len);
  var view = new DataView(buf);
  var regularChunksEnd = ((encoded.length - 4) | 0);
  var i = 0;
  var j = 0;
  var chunk = 0;
  while (true) {
    chunk = (((encoded.charCodeAt(i) | (encoded.charCodeAt(((i + 1) | 0)) << 8)) | (encoded.charCodeAt(((i + 2) | 0)) << 16)) | (encoded.charCodeAt(((i + 3) | 0)) << 24));
    chunk = ((((chunk - 808464432) | 0) - ((chunk & 1616928864) >>> 3)) | 0);
    chunk = (((chunk & 1056980736) >>> 2) | (chunk & 4128831));
    chunk = (((chunk & 268369920) >>> 4) | (chunk & 4095));
    if ((i === regularChunksEnd)) {
      break;
    }
    view.setUint32(j, chunk, true);
    i = ((i + 4) | 0);
    j = ((j + 3) | 0);
  }
  var trailing = ((len - j) | 0);
  view.setUint8(j, chunk);
  if ((trailing !== 1)) {
    view.setUint8(((j + 1) | 0), (chunk >>> 8));
    if ((trailing === 3)) {
      view.setUint8(((j + 2) | 0), (chunk >>> 16));
    }
  }
  return buf;
}
function $constArrayBuffer_S(len, encoded) {
  var buf = $constArrayBuffer_B((len << 1), encoded);
  if ($typedArraysAreBigEndian) {
    var view = new DataView(buf);
    var i = 0;
    while ((i !== len)) {
      view.putInt16(i, view.getInt16(i, true), false);
      i = ((i + 2) | 0);
    }
  }
  return buf;
}
function $constArrayBuffer_I(len, encoded) {
  var buf = $constArrayBuffer_B((len << 2), encoded);
  if ($typedArraysAreBigEndian) {
    var view = new DataView(buf);
    var i = 0;
    while ((i !== len)) {
      view.putInt32(i, view.getInt32(i, true), false);
      i = ((i + 4) | 0);
    }
  }
  return buf;
}
function $constArrayBuffer_J(len, encoded) {
  return $constArrayBuffer_I((len << 1), encoded);
}
function $constTypedArrayU_I(len, encoded, prevMask) {
  var buf = new Int32Array(len);
  var inLen = (encoded.length | 0);
  var prev = 0;
  var i = 0;
  var j = 0;
  var v = 0;
  while ((i !== inLen)) {
    var c = encoded.charCodeAt(i);
    if ((c < 80)) {
      v = ((v | (c - 48)) << 5);
    } else {
      v = (v | (c - 93));
      prev = (((prev & prevMask) + v) | 0);
      buf[j] = prev;
      j = ((j + 1) | 0);
      v = 0;
    }
    i = ((i + 1) | 0);
  }
  return buf;
}
function $constTypedArrayS_I(len, encoded, prevMask) {
  var buf = new Int32Array(len);
  var inLen = (encoded.length | 0);
  var prev = 0;
  var i = 0;
  var j = 0;
  var v = 0;
  var first = true;
  while ((i !== inLen)) {
    var c = encoded.charCodeAt(i);
    if ((c < 80)) {
      if (first) {
        v = (((c - 48) << 27) >> 22);
        first = false;
      } else {
        v = ((v | (c - 48)) << 5);
      }
    } else {
      if (first) {
        v = (((c - 93) << 27) >> 27);
      } else {
        v = (v | (c - 93));
        first = true;
      }
      prev = (((prev & prevMask) + v) | 0);
      buf[j] = prev;
      j = ((j + 1) | 0);
    }
    i = ((i + 1) | 0);
  }
  return buf;
}
function $constArrRaw_B(len, encoded) {
  return new $ac_B(new Int8Array($constArrayBuffer_B(len, encoded)));
}
function $constArrRaw_S(len, encoded) {
  return new $ac_S(new Int16Array($constArrayBuffer_S(len, encoded)));
}
function $constArrRaw_C(len, encoded) {
  return new $ac_C(new Uint16Array($constArrayBuffer_S(len, encoded)));
}
function $constArrRaw_I(len, encoded) {
  return new $ac_I(new Int32Array($constArrayBuffer_I(len, encoded)));
}
function $constArrRaw_J(len, encoded) {
  return new $ac_J(new Int32Array($constArrayBuffer_J(len, encoded)));
}
function $constArrUVals_I(len, encoded) {
  return new $ac_I($constTypedArrayU_I(len, encoded, 0));
}
function $constArrUDiffs_I(len, encoded) {
  return new $ac_I($constTypedArrayU_I(len, encoded, (-1)));
}
function $constArrSVals_I(len, encoded) {
  return new $ac_I($constTypedArrayS_I(len, encoded, 0));
}
function $constArrSDiffs_I(len, encoded) {
  return new $ac_I($constTypedArrayS_I(len, encoded, (-1)));
}
function $constArrUVals_J(len, encoded) {
  return new $ac_J($constTypedArrayU_I((len << 1), encoded, 0));
}
function $constArrUDiffs_J(len, encoded) {
  return new $ac_J($constTypedArrayU_I((len << 1), encoded, (-1)));
}
function $constArrSVals_J(len, encoded) {
  return new $ac_J($constTypedArrayS_I((len << 1), encoded, 0));
}
function $constArrSDiffs_J(len, encoded) {
  return new $ac_J($constTypedArrayS_I((len << 1), encoded, (-1)));
}
var $d_Lcom_raquo_airstream_core_InternalObserver = new $TypeData().i(1, "com.raquo.airstream.core.InternalObserver", ({
  az: 1
}));
function $f_Lcom_raquo_airstream_core_Named__defaultDisplayName__T($thiz) {
  return (($objectGetClass($thiz).j8() + "@") + $thiz.r());
}
function $f_Lcom_raquo_airstream_core_Named__displayName__T($thiz) {
  var x = $thiz.e3();
  return ((x === (void 0)) ? $thiz.e0() : x);
}
/** @constructor */
function $c_Lcom_raquo_airstream_core_Observer$() {
  $n_Lcom_raquo_airstream_core_Observer$ = this;
  $m_Lcom_raquo_airstream_core_Observer$().oq(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((_$1) => (void 0))), $m_s_PartialFunction$().gC, true);
}
$p = $c_Lcom_raquo_airstream_core_Observer$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_airstream_core_Observer$;
/** @constructor */
function $h_Lcom_raquo_airstream_core_Observer$() {
}
$h_Lcom_raquo_airstream_core_Observer$.prototype = $p;
$p.oq = (function(onNext, onError, handleObserverErrors) {
  return new $c_Lcom_raquo_airstream_core_Observer$$anon$8(onNext, handleObserverErrors, onError, this);
});
$p.q7 = (function(onTry, handleObserverErrors) {
  return new $c_Lcom_raquo_airstream_core_Observer$$anon$9(onTry, handleObserverErrors, this);
});
var $d_Lcom_raquo_airstream_core_Observer$ = new $TypeData().i($c_Lcom_raquo_airstream_core_Observer$, "com.raquo.airstream.core.Observer$", ({
  cJ: 1
}));
var $n_Lcom_raquo_airstream_core_Observer$;
function $m_Lcom_raquo_airstream_core_Observer$() {
  if ((!$n_Lcom_raquo_airstream_core_Observer$)) {
    $n_Lcom_raquo_airstream_core_Observer$ = new $c_Lcom_raquo_airstream_core_Observer$();
  }
  return $n_Lcom_raquo_airstream_core_Observer$;
}
/** @constructor */
function $c_Lcom_raquo_airstream_core_ObserverList$() {
}
$p = $c_Lcom_raquo_airstream_core_ObserverList$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_airstream_core_ObserverList$;
/** @constructor */
function $h_Lcom_raquo_airstream_core_ObserverList$() {
}
$h_Lcom_raquo_airstream_core_ObserverList$.prototype = $p;
$p.o3 = (function(this$, observer) {
  var index = (this$.indexOf(observer) | 0);
  var shouldRemove = (index !== (-1));
  if (shouldRemove) {
    this$.splice(index, 1);
  }
  return shouldRemove;
});
var $d_Lcom_raquo_airstream_core_ObserverList$ = new $TypeData().i($c_Lcom_raquo_airstream_core_ObserverList$, "com.raquo.airstream.core.ObserverList$", ({
  cM: 1
}));
var $n_Lcom_raquo_airstream_core_ObserverList$;
function $m_Lcom_raquo_airstream_core_ObserverList$() {
  if ((!$n_Lcom_raquo_airstream_core_ObserverList$)) {
    $n_Lcom_raquo_airstream_core_ObserverList$ = new $c_Lcom_raquo_airstream_core_ObserverList$();
  }
  return $n_Lcom_raquo_airstream_core_ObserverList$;
}
/** @constructor */
function $c_Lcom_raquo_airstream_core_Signal$() {
  this.ef = 0;
  this.ef = 0;
}
$p = $c_Lcom_raquo_airstream_core_Signal$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_airstream_core_Signal$;
/** @constructor */
function $h_Lcom_raquo_airstream_core_Signal$() {
}
$h_Lcom_raquo_airstream_core_Signal$.prototype = $p;
$p.nS = (function() {
  if ((this.ef === 2147483647)) {
    this.ef = 1;
  } else {
    this.ef = ((1 + this.ef) | 0);
  }
  return this.ef;
});
var $d_Lcom_raquo_airstream_core_Signal$ = new $TypeData().i($c_Lcom_raquo_airstream_core_Signal$, "com.raquo.airstream.core.Signal$", ({
  cN: 1
}));
var $n_Lcom_raquo_airstream_core_Signal$;
function $m_Lcom_raquo_airstream_core_Signal$() {
  if ((!$n_Lcom_raquo_airstream_core_Signal$)) {
    $n_Lcom_raquo_airstream_core_Signal$ = new $c_Lcom_raquo_airstream_core_Signal$();
  }
  return $n_Lcom_raquo_airstream_core_Signal$;
}
/** @constructor */
function $c_Lcom_raquo_airstream_core_Transaction(code) {
  this.hs = null;
  this.jD = null;
  this.ht = 0;
  this.hs = code;
  this.jD = (void 0);
  var x = $m_Lcom_raquo_airstream_core_Transaction$pendingTransactions$().gb();
  this.ht = ((x === (void 0)) ? 1 : ((1 + x.ht) | 0));
  if ((($m_Lcom_raquo_airstream_core_Transaction$().gl === (-1)) || (this.ht > $m_Lcom_raquo_airstream_core_Transaction$().gl))) {
    $m_Lcom_raquo_airstream_core_AirstreamError$().c2(new $c_Lcom_raquo_airstream_core_AirstreamError$TransactionDepthExceeded(this, $m_Lcom_raquo_airstream_core_Transaction$().gl));
  } else if ($m_Lcom_raquo_airstream_core_Transaction$onStart$().aY) {
    ($m_Lcom_raquo_airstream_core_Transaction$onStart$().dH.push(this) | 0);
  } else {
    $m_Lcom_raquo_airstream_core_Transaction$pendingTransactions$().iF(this);
  }
}
$p = $c_Lcom_raquo_airstream_core_Transaction.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_airstream_core_Transaction;
/** @constructor */
function $h_Lcom_raquo_airstream_core_Transaction() {
}
$h_Lcom_raquo_airstream_core_Transaction.prototype = $p;
var $d_Lcom_raquo_airstream_core_Transaction = new $TypeData().i($c_Lcom_raquo_airstream_core_Transaction, "com.raquo.airstream.core.Transaction", ({
  cO: 1
}));
/** @constructor */
function $c_Lcom_raquo_airstream_core_Transaction$() {
  this.gl = 0;
  this.jE = null;
  $n_Lcom_raquo_airstream_core_Transaction$ = this;
  this.gl = 1000;
  this.jE = new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((trx) => {
    throw $ct_jl_Exception__T__(new $c_jl_Exception(), (("Attempted to run Transaction " + trx) + " after it was already executed."));
  }));
}
$p = $c_Lcom_raquo_airstream_core_Transaction$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_airstream_core_Transaction$;
/** @constructor */
function $h_Lcom_raquo_airstream_core_Transaction$() {
}
$h_Lcom_raquo_airstream_core_Transaction$.prototype = $p;
$p.ne = (function(transaction) {
  try {
    transaction.hs.b(transaction);
    var x = transaction.jD;
    if ((x !== (void 0))) {
      while (x.rS()) {
        x.rN().rU(transaction);
      }
    }
  } catch (e) {
    var e$2 = ((e instanceof $c_jl_Throwable) ? e : new $c_sjs_js_JavaScriptException(e));
    $m_Lcom_raquo_airstream_core_AirstreamError$().c2(e$2);
  }
});
var $d_Lcom_raquo_airstream_core_Transaction$ = new $TypeData().i($c_Lcom_raquo_airstream_core_Transaction$, "com.raquo.airstream.core.Transaction$", ({
  cP: 1
}));
var $n_Lcom_raquo_airstream_core_Transaction$;
function $m_Lcom_raquo_airstream_core_Transaction$() {
  if ((!$n_Lcom_raquo_airstream_core_Transaction$)) {
    $n_Lcom_raquo_airstream_core_Transaction$ = new $c_Lcom_raquo_airstream_core_Transaction$();
  }
  return $n_Lcom_raquo_airstream_core_Transaction$;
}
function $p_Lcom_raquo_airstream_core_Transaction$onStart$__resolve__V($thiz) {
  if ((($thiz.gm.length | 0) === 0)) {
    if ((($thiz.dH.length | 0) > 0)) {
      new $c_Lcom_raquo_airstream_core_Transaction(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((_$3) => {
        while ((($thiz.dH.length | 0) > 0)) {
          $m_Lcom_raquo_airstream_core_Transaction$pendingTransactions$().iF($thiz.dH.shift());
        }
      })));
    }
  } else {
    new $c_Lcom_raquo_airstream_core_Transaction(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((trx) => {
      while ((($thiz.gm.length | 0) > 0)) {
        var callback = $thiz.gm.shift();
        try {
          callback.b(trx);
        } catch (e) {
          var e$2 = ((e instanceof $c_jl_Throwable) ? e : new $c_sjs_js_JavaScriptException(e));
          $m_Lcom_raquo_airstream_core_AirstreamError$().c2(e$2);
        }
      }
      while ((($thiz.dH.length | 0) > 0)) {
        var _trx = $thiz.dH.shift();
        $m_Lcom_raquo_airstream_core_Transaction$pendingTransactions$().iF(_trx);
      }
    })));
  }
}
/** @constructor */
function $c_Lcom_raquo_airstream_core_Transaction$onStart$() {
  this.aY = false;
  this.gm = null;
  this.dH = null;
  $n_Lcom_raquo_airstream_core_Transaction$onStart$ = this;
  this.aY = false;
  this.gm = $m_Lcom_raquo_ew_JsArray$().bb($m_sr_ScalaRunTime$().b4(new ($d_F1.r().C)([])));
  this.dH = $m_Lcom_raquo_ew_JsArray$().bb($m_sr_ScalaRunTime$().b4(new ($d_Lcom_raquo_airstream_core_Transaction.r().C)([])));
}
$p = $c_Lcom_raquo_airstream_core_Transaction$onStart$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_airstream_core_Transaction$onStart$;
/** @constructor */
function $h_Lcom_raquo_airstream_core_Transaction$onStart$() {
}
$h_Lcom_raquo_airstream_core_Transaction$onStart$.prototype = $p;
var $d_Lcom_raquo_airstream_core_Transaction$onStart$ = new $TypeData().i($c_Lcom_raquo_airstream_core_Transaction$onStart$, "com.raquo.airstream.core.Transaction$onStart$", ({
  cQ: 1
}));
var $n_Lcom_raquo_airstream_core_Transaction$onStart$;
function $m_Lcom_raquo_airstream_core_Transaction$onStart$() {
  if ((!$n_Lcom_raquo_airstream_core_Transaction$onStart$)) {
    $n_Lcom_raquo_airstream_core_Transaction$onStart$ = new $c_Lcom_raquo_airstream_core_Transaction$onStart$();
  }
  return $n_Lcom_raquo_airstream_core_Transaction$onStart$;
}
function $p_Lcom_raquo_airstream_core_Transaction$pendingTransactions$__maybeChildrenFor__Lcom_raquo_airstream_core_Transaction__O($thiz, transaction) {
  return $thiz.dI.get(transaction);
}
function $p_Lcom_raquo_airstream_core_Transaction$pendingTransactions$__pushToStack__Lcom_raquo_airstream_core_Transaction__V($thiz, transaction) {
  $thiz.gn.unshift(transaction);
}
function $p_Lcom_raquo_airstream_core_Transaction$pendingTransactions$__popStack__O($thiz) {
  return $thiz.gn.shift();
}
function $p_Lcom_raquo_airstream_core_Transaction$pendingTransactions$__enqueueChild__Lcom_raquo_airstream_core_Transaction__Lcom_raquo_airstream_core_Transaction__V($thiz, parent, newChild) {
  var maybeChildren = $p_Lcom_raquo_airstream_core_Transaction$pendingTransactions$__maybeChildrenFor__Lcom_raquo_airstream_core_Transaction__O($thiz, parent);
  var noChildrenFound = (maybeChildren === (void 0));
  var newChildren = ((maybeChildren === (void 0)) ? $m_Lcom_raquo_ew_JsArray$().bb($m_sr_ScalaRunTime$().b4(new ($d_Lcom_raquo_airstream_core_Transaction.r().C)([]))) : maybeChildren);
  newChildren.push(newChild);
  if (noChildrenFound) {
    $thiz.dI.set(parent, newChildren);
  }
}
function $p_Lcom_raquo_airstream_core_Transaction$pendingTransactions$__dequeueChild__Lcom_raquo_airstream_core_Transaction__O($thiz, parent) {
  var maybeParentChildren = $p_Lcom_raquo_airstream_core_Transaction$pendingTransactions$__maybeChildrenFor__Lcom_raquo_airstream_core_Transaction__O($thiz, parent);
  var x = (((maybeParentChildren === (void 0)) || ((maybeParentChildren.length | 0) > 0)) ? maybeParentChildren : (void 0));
  if ((x === (void 0))) {
    return (void 0);
  } else {
    var nextChild = x.shift();
    if (((x.length | 0) === 0)) {
      (!(!$thiz.dI.delete(parent)));
    }
    return nextChild;
  }
}
/** @constructor */
function $c_Lcom_raquo_airstream_core_Transaction$pendingTransactions$() {
  this.gn = null;
  this.dI = null;
  $n_Lcom_raquo_airstream_core_Transaction$pendingTransactions$ = this;
  this.gn = $m_Lcom_raquo_ew_JsArray$().bb($m_sr_ScalaRunTime$().b4(new ($d_Lcom_raquo_airstream_core_Transaction.r().C)([])));
  this.dI = new Map();
}
$p = $c_Lcom_raquo_airstream_core_Transaction$pendingTransactions$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_airstream_core_Transaction$pendingTransactions$;
/** @constructor */
function $h_Lcom_raquo_airstream_core_Transaction$pendingTransactions$() {
}
$h_Lcom_raquo_airstream_core_Transaction$pendingTransactions$.prototype = $p;
$p.iF = (function(newTransaction) {
  var x = this.gb();
  if ((x === (void 0))) {
    $p_Lcom_raquo_airstream_core_Transaction$pendingTransactions$__pushToStack__Lcom_raquo_airstream_core_Transaction__V(this, newTransaction);
    $m_Lcom_raquo_airstream_core_Transaction$().ne(newTransaction);
    this.pN(newTransaction);
  } else {
    $p_Lcom_raquo_airstream_core_Transaction$pendingTransactions$__enqueueChild__Lcom_raquo_airstream_core_Transaction__Lcom_raquo_airstream_core_Transaction__V(this, x, newTransaction);
  }
});
$p.pN = (function(transaction) {
  var transaction$tailLocal1 = transaction;
  while (true) {
    var x = this.gb();
    var elem = transaction$tailLocal1;
    if ((!((x !== (void 0)) && $m_sr_BoxesRunTime$().j(elem, x)))) {
      throw $ct_jl_Exception__T__(new $c_jl_Exception(), "Transaction queue error: Completed transaction is not the first in stack. This is a bug in Airstream.");
    }
    this.qR(transaction$tailLocal1);
    transaction$tailLocal1.hs = $m_Lcom_raquo_airstream_core_Transaction$().jE;
    var maybeNextTransaction = this.gb();
    if ($m_sr_BoxesRunTime$().j(maybeNextTransaction, (void 0))) {
      if (((this.dI.size | 0) > 0)) {
        var numChildren = new $c_sr_IntRef(0);
        this.dI.forEach(((numChildren) => ((transactions, _$4) => {
          var ev$12 = ((numChildren.ab + (transactions.length | 0)) | 0);
          numChildren.ab = ev$12;
        }))(numChildren));
        throw $ct_jl_Exception__T__(new $c_jl_Exception(), (((("Transaction queue error: Stack cleared, but a total of " + numChildren.ab) + " children for ") + (this.dI.size | 0)) + " transactions remain. This is a bug in Airstream."));
      } else {
        return (void 0);
      }
    } else {
      $m_Lcom_raquo_airstream_core_Transaction$().ne(maybeNextTransaction);
      transaction$tailLocal1 = maybeNextTransaction;
    }
  }
});
$p.qR = (function(doneTransaction) {
  var doneTransaction$tailLocal1 = doneTransaction;
  while (true) {
    var maybeNextChildTrx = $p_Lcom_raquo_airstream_core_Transaction$pendingTransactions$__dequeueChild__Lcom_raquo_airstream_core_Transaction__O(this, doneTransaction$tailLocal1);
    if ($m_sr_BoxesRunTime$().j(maybeNextChildTrx, (void 0))) {
      $p_Lcom_raquo_airstream_core_Transaction$pendingTransactions$__popStack__O(this);
      var maybeParentTransaction = this.gb();
      if ((!$m_sr_BoxesRunTime$().j(maybeParentTransaction, (void 0)))) {
        doneTransaction$tailLocal1 = maybeParentTransaction;
      } else {
        return (void 0);
      }
    } else {
      $p_Lcom_raquo_airstream_core_Transaction$pendingTransactions$__pushToStack__Lcom_raquo_airstream_core_Transaction__V(this, maybeNextChildTrx);
      return (void 0);
    }
  }
});
$p.gb = (function() {
  return this.gn[0];
});
var $d_Lcom_raquo_airstream_core_Transaction$pendingTransactions$ = new $TypeData().i($c_Lcom_raquo_airstream_core_Transaction$pendingTransactions$, "com.raquo.airstream.core.Transaction$pendingTransactions$", ({
  cR: 1
}));
var $n_Lcom_raquo_airstream_core_Transaction$pendingTransactions$;
function $m_Lcom_raquo_airstream_core_Transaction$pendingTransactions$() {
  if ((!$n_Lcom_raquo_airstream_core_Transaction$pendingTransactions$)) {
    $n_Lcom_raquo_airstream_core_Transaction$pendingTransactions$ = new $c_Lcom_raquo_airstream_core_Transaction$pendingTransactions$();
  }
  return $n_Lcom_raquo_airstream_core_Transaction$pendingTransactions$;
}
/** @constructor */
function $c_Lcom_raquo_airstream_custom_CustomSource$Config(onWillStart, onStart, onStop) {
  this.jI = null;
  this.jG = null;
  this.jH = null;
  this.jI = onWillStart;
  this.jG = onStart;
  this.jH = onStop;
}
$p = $c_Lcom_raquo_airstream_custom_CustomSource$Config.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_airstream_custom_CustomSource$Config;
/** @constructor */
function $h_Lcom_raquo_airstream_custom_CustomSource$Config() {
}
$h_Lcom_raquo_airstream_custom_CustomSource$Config.prototype = $p;
var $d_Lcom_raquo_airstream_custom_CustomSource$Config = new $TypeData().i($c_Lcom_raquo_airstream_custom_CustomSource$Config, "com.raquo.airstream.custom.CustomSource$Config", ({
  cU: 1
}));
/** @constructor */
function $c_Lcom_raquo_airstream_custom_CustomSource$Config$() {
}
$p = $c_Lcom_raquo_airstream_custom_CustomSource$Config$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_airstream_custom_CustomSource$Config$;
/** @constructor */
function $h_Lcom_raquo_airstream_custom_CustomSource$Config$() {
}
$h_Lcom_raquo_airstream_custom_CustomSource$Config$.prototype = $p;
$p.pe = (function(onStart, onStop) {
  return new $c_Lcom_raquo_airstream_custom_CustomSource$Config(new $c_sjsr_AnonFunction0_$$Lambda$2bf0f8dc580d6edeb2d6a336c52a1bab3049702d((() => (void 0))), onStart, onStop);
});
var $d_Lcom_raquo_airstream_custom_CustomSource$Config$ = new $TypeData().i($c_Lcom_raquo_airstream_custom_CustomSource$Config$, "com.raquo.airstream.custom.CustomSource$Config$", ({
  cV: 1
}));
var $n_Lcom_raquo_airstream_custom_CustomSource$Config$;
function $m_Lcom_raquo_airstream_custom_CustomSource$Config$() {
  if ((!$n_Lcom_raquo_airstream_custom_CustomSource$Config$)) {
    $n_Lcom_raquo_airstream_custom_CustomSource$Config$ = new $c_Lcom_raquo_airstream_custom_CustomSource$Config$();
  }
  return $n_Lcom_raquo_airstream_custom_CustomSource$Config$;
}
function $p_Lcom_raquo_airstream_ownership_DynamicOwner__removeSubscriptionNow__Lcom_raquo_airstream_ownership_DynamicSubscription__V($thiz, subscription) {
  var index = ($thiz.d0.indexOf(subscription) | 0);
  if ((index !== (-1))) {
    $thiz.d0.splice(index, 1);
    if ((!$thiz.bz.c())) {
      subscription.nY();
    }
  } else {
    throw $ct_jl_Exception__T__(new $c_jl_Exception(), "Can not remove DynamicSubscription from DynamicOwner: subscription not found. Did you already kill it?");
  }
}
function $p_Lcom_raquo_airstream_ownership_DynamicOwner__removePendingSubscriptionsNow__V($thiz) {
  while ((($thiz.gs.length | 0) > 0)) {
    $p_Lcom_raquo_airstream_ownership_DynamicOwner__removeSubscriptionNow__Lcom_raquo_airstream_ownership_DynamicSubscription__V($thiz, $thiz.gs.shift());
  }
}
/** @constructor */
function $c_Lcom_raquo_airstream_ownership_DynamicOwner(onAccessAfterKilled) {
  this.k5 = null;
  this.d0 = null;
  this.eg = false;
  this.gs = null;
  this.bz = null;
  this.eh = 0;
  this.k5 = onAccessAfterKilled;
  this.d0 = $m_Lcom_raquo_ew_JsArray$().bb($m_sr_ScalaRunTime$().b4(new ($d_Lcom_raquo_airstream_ownership_DynamicSubscription.r().C)([])));
  this.eg = true;
  this.gs = $m_Lcom_raquo_ew_JsArray$().bb($m_sr_ScalaRunTime$().b4(new ($d_Lcom_raquo_airstream_ownership_DynamicSubscription.r().C)([])));
  this.bz = $m_s_None$();
  this.eh = 0;
}
$p = $c_Lcom_raquo_airstream_ownership_DynamicOwner.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_airstream_ownership_DynamicOwner;
/** @constructor */
function $h_Lcom_raquo_airstream_ownership_DynamicOwner() {
}
$h_Lcom_raquo_airstream_ownership_DynamicOwner.prototype = $p;
$p.mX = (function() {
  if ((!(!this.bz.c()))) {
    var this$4 = $m_Lcom_raquo_airstream_core_Transaction$onStart$();
    var f = (() => {
      var newOwner = new $c_Lcom_raquo_airstream_ownership_OneTimeOwner(this.k5);
      this.bz = new $c_s_Some(newOwner);
      this.eg = false;
      this.eh = 0;
      var i = 0;
      var originalNumSubs = (this.d0.length | 0);
      while ((i < originalNumSubs)) {
        var ix = ((i + this.eh) | 0);
        this.d0[ix].nU(newOwner);
        i = ((1 + i) | 0);
      }
      $p_Lcom_raquo_airstream_ownership_DynamicOwner__removePendingSubscriptionsNow__V(this);
      this.eg = true;
      this.eh = 0;
    });
    $m_Lcom_raquo_airstream_core_Transaction$onStart$();
    var when = true;
    if ((this$4.aY || (!when))) {
      f();
    } else {
      this$4.aY = true;
      try {
        f();
      } finally {
        this$4.aY = false;
        $p_Lcom_raquo_airstream_core_Transaction$onStart$__resolve__V(this$4);
      }
    }
  } else {
    throw $ct_jl_Exception__T__(new $c_jl_Exception(), (("Can not activate " + this) + ": it is already active"));
  }
});
$p.pF = (function() {
  if ((!this.bz.c())) {
    this.eg = false;
    var arr = this.d0;
    var i = 0;
    var len = (arr.length | 0);
    while ((i < len)) {
      arr[i].nY();
      i = ((1 + i) | 0);
    }
    $p_Lcom_raquo_airstream_ownership_DynamicOwner__removePendingSubscriptionsNow__V(this);
    var this$4 = this.bz;
    if ((!this$4.c())) {
      this$4.s().nM();
    }
    $p_Lcom_raquo_airstream_ownership_DynamicOwner__removePendingSubscriptionsNow__V(this);
    this.eg = true;
    this.bz = $m_s_None$();
  } else {
    throw $ct_jl_Exception__T__(new $c_jl_Exception(), "Can not deactivate DynamicOwner: it is not active");
  }
});
$p.p6 = (function(subscription, prepend) {
  if (prepend) {
    this.eh = ((1 + this.eh) | 0);
    this.d0.unshift(subscription);
  } else {
    this.d0.push(subscription);
  }
  var this$1 = this.bz;
  if ((!this$1.c())) {
    var x0 = this$1.s();
    subscription.nU(x0);
  }
});
$p.qZ = (function(subscription) {
  if (this.eg) {
    $p_Lcom_raquo_airstream_ownership_DynamicOwner__removeSubscriptionNow__Lcom_raquo_airstream_ownership_DynamicSubscription__V(this, subscription);
  } else {
    this.gs.push(subscription);
  }
});
var $d_Lcom_raquo_airstream_ownership_DynamicOwner = new $TypeData().i($c_Lcom_raquo_airstream_ownership_DynamicOwner, "com.raquo.airstream.ownership.DynamicOwner", ({
  cZ: 1
}));
/** @constructor */
function $c_Lcom_raquo_airstream_ownership_DynamicSubscription(dynamicOwner, activate, prepend) {
  this.gt = null;
  this.k6 = null;
  this.gu = null;
  this.gt = dynamicOwner;
  this.k6 = activate;
  this.gu = $m_s_None$();
  dynamicOwner.p6(this, prepend);
}
$p = $c_Lcom_raquo_airstream_ownership_DynamicSubscription.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_airstream_ownership_DynamicSubscription;
/** @constructor */
function $h_Lcom_raquo_airstream_ownership_DynamicSubscription() {
}
$h_Lcom_raquo_airstream_ownership_DynamicSubscription.prototype = $p;
$p.hb = (function() {
  this.gt.qZ(this);
});
$p.nU = (function(owner) {
  var this$2 = $m_Lcom_raquo_airstream_core_Transaction$onStart$();
  var f = (() => {
    this.gu = this.k6.b(owner);
  });
  $m_Lcom_raquo_airstream_core_Transaction$onStart$();
  var when = true;
  if ((this$2.aY || (!when))) {
    f();
  } else {
    this$2.aY = true;
    try {
      f();
    } finally {
      this$2.aY = false;
      $p_Lcom_raquo_airstream_core_Transaction$onStart$__resolve__V(this$2);
    }
  }
});
$p.nY = (function() {
  var this$1 = this.gu;
  if ((!this$1.c())) {
    this$1.s().hb();
    this.gu = $m_s_None$();
  }
});
var $d_Lcom_raquo_airstream_ownership_DynamicSubscription = new $TypeData().i($c_Lcom_raquo_airstream_ownership_DynamicSubscription, "com.raquo.airstream.ownership.DynamicSubscription", ({
  d0: 1
}));
/** @constructor */
function $c_Lcom_raquo_airstream_ownership_DynamicSubscription$() {
}
$p = $c_Lcom_raquo_airstream_ownership_DynamicSubscription$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_airstream_ownership_DynamicSubscription$;
/** @constructor */
function $h_Lcom_raquo_airstream_ownership_DynamicSubscription$() {
}
$h_Lcom_raquo_airstream_ownership_DynamicSubscription$.prototype = $p;
$p.gk = (function(dynamicOwner, activate, prepend) {
  return new $c_Lcom_raquo_airstream_ownership_DynamicSubscription(dynamicOwner, new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((owner) => new $c_s_Some(activate.b(owner)))), prepend);
});
$p.og = (function(dynamicOwner, activate, prepend) {
  return new $c_Lcom_raquo_airstream_ownership_DynamicSubscription(dynamicOwner, new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((owner) => {
    activate.b(owner);
    return $m_s_None$();
  })), prepend);
});
$p.rh = (function(dynamicOwner, observable, onNext) {
  return $m_Lcom_raquo_airstream_ownership_DynamicSubscription$().gk(dynamicOwner, new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((owner) => $f_Lcom_raquo_airstream_core_BaseObservable__foreach__F1__Lcom_raquo_airstream_ownership_Owner__Lcom_raquo_airstream_ownership_Subscription(observable, onNext, owner))), false);
});
var $d_Lcom_raquo_airstream_ownership_DynamicSubscription$ = new $TypeData().i($c_Lcom_raquo_airstream_ownership_DynamicSubscription$, "com.raquo.airstream.ownership.DynamicSubscription$", ({
  d1: 1
}));
var $n_Lcom_raquo_airstream_ownership_DynamicSubscription$;
function $m_Lcom_raquo_airstream_ownership_DynamicSubscription$() {
  if ((!$n_Lcom_raquo_airstream_ownership_DynamicSubscription$)) {
    $n_Lcom_raquo_airstream_ownership_DynamicSubscription$ = new $c_Lcom_raquo_airstream_ownership_DynamicSubscription$();
  }
  return $n_Lcom_raquo_airstream_ownership_DynamicSubscription$;
}
function $f_Lcom_raquo_airstream_ownership_Owner__$init$__V($thiz) {
  $thiz.nf($m_Lcom_raquo_ew_JsArray$().bb($m_sr_ScalaRunTime$().b4(new ($d_Lcom_raquo_airstream_ownership_Subscription.r().C)([]))));
}
function $f_Lcom_raquo_airstream_ownership_Owner__killSubscriptions__V($thiz) {
  var arr = $thiz.eX();
  var i = 0;
  var len = (arr.length | 0);
  while ((i < len)) {
    $p_Lcom_raquo_airstream_ownership_Subscription__safeCleanup__V(arr[i]);
    i = ((1 + i) | 0);
  }
  $thiz.eX().length = 0;
}
function $f_Lcom_raquo_airstream_ownership_Owner__onKilledExternally__Lcom_raquo_airstream_ownership_Subscription__V($thiz, subscription) {
  var index = ($thiz.eX().indexOf(subscription) | 0);
  if ((index !== (-1))) {
    $thiz.eX().splice(index, 1);
  } else {
    throw $ct_jl_Exception__T__(new $c_jl_Exception(), "Can not remove Subscription from Owner: subscription not found.");
  }
}
function $f_Lcom_raquo_airstream_ownership_Owner__own__Lcom_raquo_airstream_ownership_Subscription__V($thiz, subscription) {
  $thiz.eX().push(subscription);
}
function $p_Lcom_raquo_airstream_ownership_Subscription__safeCleanup__V($thiz) {
  if ((!$thiz.hA)) {
    $thiz.k9.F();
    $thiz.hA = true;
  } else {
    throw $ct_jl_Exception__T__(new $c_jl_Exception(), "Can not kill Subscription: it was already killed.");
  }
}
/** @constructor */
function $c_Lcom_raquo_airstream_ownership_Subscription(owner, cleanup) {
  this.ka = null;
  this.k9 = null;
  this.hA = false;
  this.ka = owner;
  this.k9 = cleanup;
  this.hA = false;
  owner.o1(this);
}
$p = $c_Lcom_raquo_airstream_ownership_Subscription.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_airstream_ownership_Subscription;
/** @constructor */
function $h_Lcom_raquo_airstream_ownership_Subscription() {
}
$h_Lcom_raquo_airstream_ownership_Subscription.prototype = $p;
$p.hb = (function() {
  $p_Lcom_raquo_airstream_ownership_Subscription__safeCleanup__V(this);
  $f_Lcom_raquo_airstream_ownership_Owner__onKilledExternally__Lcom_raquo_airstream_ownership_Subscription__V(this.ka, this);
});
var $d_Lcom_raquo_airstream_ownership_Subscription = new $TypeData().i($c_Lcom_raquo_airstream_ownership_Subscription, "com.raquo.airstream.ownership.Subscription", ({
  d3: 1
}));
/** @constructor */
function $c_Lcom_raquo_airstream_ownership_TransferableSubscription(activate, deactivate) {
  this.kb = null;
  this.kc = null;
  this.d1 = null;
  this.dJ = false;
  this.kb = activate;
  this.kc = deactivate;
  this.d1 = $m_s_None$();
  this.dJ = false;
}
$p = $c_Lcom_raquo_airstream_ownership_TransferableSubscription.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_airstream_ownership_TransferableSubscription;
/** @constructor */
function $h_Lcom_raquo_airstream_ownership_TransferableSubscription() {
}
$h_Lcom_raquo_airstream_ownership_TransferableSubscription.prototype = $p;
$p.qt = (function() {
  var this$1 = this.d1;
  return ((!this$1.c()) && (!this$1.s().gt.bz.c()));
});
$p.rc = (function(nextOwner) {
  if (this.dJ) {
    throw $ct_jl_Exception__T__(new $c_jl_Exception(), "Unable to set owner on DynamicTransferableSubscription while a transfer on this subscription is already in progress.");
  }
  var this$1 = this.d1;
  if ((!this$1.c())) {
    var x0 = this$1.s();
    var x$2 = x0.gt;
    var $x_1 = ((nextOwner === null) ? (x$2 === null) : (nextOwner === x$2));
  } else {
    var $x_1 = false;
  }
  if ((!$x_1)) {
    if ((this.qt() && (!nextOwner.bz.c()))) {
      this.dJ = true;
    }
    var this$3 = this.d1;
    if ((!this$3.c())) {
      this$3.s().hb();
      this.d1 = $m_s_None$();
    }
    var newPilotSubscription = $m_Lcom_raquo_airstream_ownership_DynamicSubscription$().gk(nextOwner, new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((parentOwner) => {
      if ((!this.dJ)) {
        this.kb.F();
      }
      return new $c_Lcom_raquo_airstream_ownership_Subscription(parentOwner, new $c_sjsr_AnonFunction0_$$Lambda$2bf0f8dc580d6edeb2d6a336c52a1bab3049702d((() => {
        if ((!this.dJ)) {
          this.kc.F();
        }
      })));
    })), false);
    this.d1 = new $c_s_Some(newPilotSubscription);
    this.dJ = false;
  }
});
$p.ps = (function() {
  if (this.dJ) {
    throw $ct_jl_Exception__T__(new $c_jl_Exception(), "Unable to clear owner on DynamicTransferableSubscription while a transfer on this subscription is already in progress.");
  }
  var this$1 = this.d1;
  if ((!this$1.c())) {
    this$1.s().hb();
  }
  this.d1 = $m_s_None$();
});
var $d_Lcom_raquo_airstream_ownership_TransferableSubscription = new $TypeData().i($c_Lcom_raquo_airstream_ownership_TransferableSubscription, "com.raquo.airstream.ownership.TransferableSubscription", ({
  d4: 1
}));
/** @constructor */
function $c_Lcom_raquo_airstream_state_Var$() {
}
$p = $c_Lcom_raquo_airstream_state_Var$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_airstream_state_Var$;
/** @constructor */
function $h_Lcom_raquo_airstream_state_Var$() {
}
$h_Lcom_raquo_airstream_state_Var$.prototype = $p;
$p.eN = (function(initial) {
  return new $c_Lcom_raquo_airstream_state_SourceVar(new $c_s_util_Success(initial));
});
var $d_Lcom_raquo_airstream_state_Var$ = new $TypeData().i($c_Lcom_raquo_airstream_state_Var$, "com.raquo.airstream.state.Var$", ({
  d8: 1
}));
var $n_Lcom_raquo_airstream_state_Var$;
function $m_Lcom_raquo_airstream_state_Var$() {
  if ((!$n_Lcom_raquo_airstream_state_Var$)) {
    $n_Lcom_raquo_airstream_state_Var$ = new $c_Lcom_raquo_airstream_state_Var$();
  }
  return $n_Lcom_raquo_airstream_state_Var$;
}
/** @constructor */
function $c_Lcom_raquo_airstream_web_DomEventStream$() {
}
$p = $c_Lcom_raquo_airstream_web_DomEventStream$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_airstream_web_DomEventStream$;
/** @constructor */
function $h_Lcom_raquo_airstream_web_DomEventStream$() {
}
$h_Lcom_raquo_airstream_web_DomEventStream$.prototype = $p;
$p.pd = (function(eventTarget, eventKey, useCapture) {
  return new $c_Lcom_raquo_airstream_custom_CustomStreamSource(new $c_sjsr_AnonFunction4_$$Lambda$120c664e6fb20e1c3552e9e8baf775b7682c102c(((fireValue, _$1, _$2, _$3) => {
    var eventHandler = $m_sjs_js_Any$().nA(fireValue);
    return $m_Lcom_raquo_airstream_custom_CustomSource$Config$().pe(new $c_sjsr_AnonFunction0_$$Lambda$2bf0f8dc580d6edeb2d6a336c52a1bab3049702d((() => {
      eventTarget.addEventListener(eventKey, eventHandler, useCapture);
    })), new $c_sjsr_AnonFunction0_$$Lambda$2bf0f8dc580d6edeb2d6a336c52a1bab3049702d((() => {
      eventTarget.removeEventListener(eventKey, eventHandler, useCapture);
    })));
  })));
});
var $d_Lcom_raquo_airstream_web_DomEventStream$ = new $TypeData().i($c_Lcom_raquo_airstream_web_DomEventStream$, "com.raquo.airstream.web.DomEventStream$", ({
  db: 1
}));
var $n_Lcom_raquo_airstream_web_DomEventStream$;
function $m_Lcom_raquo_airstream_web_DomEventStream$() {
  if ((!$n_Lcom_raquo_airstream_web_DomEventStream$)) {
    $n_Lcom_raquo_airstream_web_DomEventStream$ = new $c_Lcom_raquo_airstream_web_DomEventStream$();
  }
  return $n_Lcom_raquo_airstream_web_DomEventStream$;
}
/** @constructor */
function $c_Lcom_raquo_ew_JsArray$() {
}
$p = $c_Lcom_raquo_ew_JsArray$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_ew_JsArray$;
/** @constructor */
function $h_Lcom_raquo_ew_JsArray$() {
}
$h_Lcom_raquo_ew_JsArray$.prototype = $p;
$p.bb = (function(items) {
  return [...$m_sjsr_Compat$().rz(items)];
});
var $d_Lcom_raquo_ew_JsArray$ = new $TypeData().i($c_Lcom_raquo_ew_JsArray$, "com.raquo.ew.JsArray$", ({
  dc: 1
}));
var $n_Lcom_raquo_ew_JsArray$;
function $m_Lcom_raquo_ew_JsArray$() {
  if ((!$n_Lcom_raquo_ew_JsArray$)) {
    $n_Lcom_raquo_ew_JsArray$ = new $c_Lcom_raquo_ew_JsArray$();
  }
  return $n_Lcom_raquo_ew_JsArray$;
}
/** @constructor */
function $c_Lcom_raquo_ew_JsArray$RichJsArray$() {
}
$p = $c_Lcom_raquo_ew_JsArray$RichJsArray$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_ew_JsArray$RichJsArray$;
/** @constructor */
function $h_Lcom_raquo_ew_JsArray$RichJsArray$() {
}
$h_Lcom_raquo_ew_JsArray$RichJsArray$.prototype = $p;
$p.qj = (function(this$, item, fromIndex) {
  return ((this$.indexOf(item, fromIndex) | 0) !== (-1));
});
$p.pY = (function(this$, cb) {
  var i = 0;
  var len = (this$.length | 0);
  while ((i < len)) {
    cb(this$[i]);
    i = ((1 + i) | 0);
  }
});
var $d_Lcom_raquo_ew_JsArray$RichJsArray$ = new $TypeData().i($c_Lcom_raquo_ew_JsArray$RichJsArray$, "com.raquo.ew.JsArray$RichJsArray$", ({
  dd: 1
}));
var $n_Lcom_raquo_ew_JsArray$RichJsArray$;
function $m_Lcom_raquo_ew_JsArray$RichJsArray$() {
  if ((!$n_Lcom_raquo_ew_JsArray$RichJsArray$)) {
    $n_Lcom_raquo_ew_JsArray$RichJsArray$ = new $c_Lcom_raquo_ew_JsArray$RichJsArray$();
  }
  return $n_Lcom_raquo_ew_JsArray$RichJsArray$;
}
/** @constructor */
function $c_Lcom_raquo_laminar_DomApi$() {
  this.ko = null;
  $n_Lcom_raquo_laminar_DomApi$ = this;
  document.createElement("template");
  this.pD($m_Lcom_raquo_laminar_api_package$().o.rm().rn());
  this.ko = new RegExp(" ", "g");
}
$p = $c_Lcom_raquo_laminar_DomApi$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_DomApi$;
/** @constructor */
function $h_Lcom_raquo_laminar_DomApi$() {
}
$h_Lcom_raquo_laminar_DomApi$.prototype = $p;
$p.p7 = (function(parent, child) {
  try {
    parent.appendChild(child);
    return true;
  } catch (e) {
    var e$2 = ((e instanceof $c_jl_Throwable) ? e : new $c_sjs_js_JavaScriptException(e));
    if (((e$2 instanceof $c_sjs_js_JavaScriptException) && (!(!(e$2.K instanceof DOMException))))) {
      return false;
    }
    throw ((e$2 instanceof $c_sjs_js_JavaScriptException) ? e$2.K : e$2);
  }
});
$p.qW = (function(parent, child) {
  try {
    parent.removeChild(child);
    return true;
  } catch (e) {
    var e$2 = ((e instanceof $c_jl_Throwable) ? e : new $c_sjs_js_JavaScriptException(e));
    if (((e$2 instanceof $c_sjs_js_JavaScriptException) && (!(!(e$2.K instanceof DOMException))))) {
      return false;
    }
    throw ((e$2 instanceof $c_sjs_js_JavaScriptException) ? e$2.K : e$2);
  }
});
$p.qp = (function(parent, newChild, referenceChild) {
  try {
    parent.insertBefore(newChild, referenceChild);
    return true;
  } catch (e) {
    var e$2 = ((e instanceof $c_jl_Throwable) ? e : new $c_sjs_js_JavaScriptException(e));
    if (((e$2 instanceof $c_sjs_js_JavaScriptException) && (!(!(e$2.K instanceof DOMException))))) {
      return false;
    }
    throw ((e$2 instanceof $c_sjs_js_JavaScriptException) ? e$2.K : e$2);
  }
});
$p.qo = (function(parent, newChild, referenceChild) {
  try {
    parent.insertBefore(newChild, referenceChild.nextSibling);
    return true;
  } catch (e) {
    var e$2 = ((e instanceof $c_jl_Throwable) ? e : new $c_sjs_js_JavaScriptException(e));
    if (((e$2 instanceof $c_sjs_js_JavaScriptException) && (!(!(e$2.K instanceof DOMException))))) {
      return false;
    }
    throw ((e$2 instanceof $c_sjs_js_JavaScriptException) ? e$2.K : e$2);
  }
});
$p.r1 = (function(parent, newChild, oldChild) {
  try {
    parent.replaceChild(newChild, oldChild);
    return true;
  } catch (e) {
    var e$2 = ((e instanceof $c_jl_Throwable) ? e : new $c_sjs_js_JavaScriptException(e));
    if (((e$2 instanceof $c_sjs_js_JavaScriptException) && (!(!(e$2.K instanceof DOMException))))) {
      return false;
    }
    throw ((e$2 instanceof $c_sjs_js_JavaScriptException) ? e$2.K : e$2);
  }
});
$p.qw = (function(node, ancestor) {
  var node$tailLocal1 = node;
  while (true) {
    if ((node$tailLocal1.parentNode !== null)) {
      var effectiveParentNode = node$tailLocal1.parentNode;
    } else {
      var maybeShadowHost = node$tailLocal1.host;
      var effectiveParentNode = ((maybeShadowHost === (void 0)) ? null : maybeShadowHost);
    }
    if ((effectiveParentNode === null)) {
      return false;
    }
    if ($m_sr_BoxesRunTime$().j(ancestor, effectiveParentNode)) {
      return true;
    }
    node$tailLocal1 = effectiveParentNode;
  }
});
$p.oW = (function(element, listener) {
  element.addEventListener(listener.ej.ei.f9, listener.hS, listener.hT);
});
$p.qX = (function(element, listener) {
  element.removeEventListener(listener.ej.ei.f9, listener.hS, listener.hT);
});
$p.pC = (function(tag) {
  return document.createElement(tag.i2);
});
$p.q9 = (function(element, attr) {
  var x = this.qa(element, attr);
  return ((x === (void 0)) ? (void 0) : attr.hM.iR(x));
});
$p.qa = (function(element, attr) {
  var domValue = element.b5.getAttributeNS(null, attr.fa);
  return ((domValue !== null) ? domValue : (void 0));
});
$p.ra = (function(element, attr, value) {
  this.rb(element, attr, attr.hM.g1(value));
});
$p.rb = (function(element, attr, domValue) {
  if ((domValue === null)) {
    this.qY(element, attr);
  } else {
    element.b5.setAttribute(attr.fa, domValue);
  }
});
$p.qY = (function(element, attr) {
  element.b5.removeAttribute(attr.fa);
});
$p.qb = (function(element, prop) {
  return element.b5[prop.cB];
});
$p.od = (function(element, prop, value) {
  this.oe(element, prop, prop.hN.g1(value));
});
$p.oe = (function(element, prop, value) {
  element.b5[prop.cB] = value;
});
$p.pD = (function(tag) {
  return document.createElementNS("http://www.w3.org/2000/svg", tag.lL);
});
$p.qd = (function(element, attr) {
  var x = this.qe(element, attr);
  return ((x === (void 0)) ? (void 0) : attr.hO.iR(x));
});
$p.qe = (function(element, attr) {
  var $x_2 = element.jq();
  var this$1 = attr.gy;
  var $x_1 = $x_2.getAttributeNS((this$1.c() ? null : this$1.s()), attr.hP);
  var domValue = $x_1;
  return ((domValue !== null) ? domValue : (void 0));
});
$p.rd = (function(element, attr, value) {
  this.re(element, attr, attr.hO.g1(value));
});
$p.re = (function(element, attr, domValue) {
  if ((domValue === null)) {
    this.r0(element, attr);
  } else {
    var this$1 = attr.gy;
    if (this$1.c()) {
      element.jq().setAttribute(attr.gx, domValue);
    } else {
      var x0 = this$1.s();
      element.jq().setAttributeNS(x0, attr.gx, domValue);
    }
  }
});
$p.r0 = (function(element, attr) {
  var $x_1 = element.jq();
  var this$1 = attr.gy;
  $x_1.removeAttributeNS((this$1.c() ? null : this$1.s()), attr.hP);
});
$p.pB = (function(text) {
  return document.createComment(text);
});
$p.pE = (function(text) {
  return document.createTextNode(text);
});
$p.nG = (function(element) {
  return $m_sc_StringOps$().pv(element.tagName, 45);
});
$p.qf = (function(element) {
  if ((!(!(element instanceof HTMLInputElement)))) {
    return element.value;
  } else if ((!(!(element instanceof HTMLTextAreaElement)))) {
    return element.value;
  } else if ((!(!(element instanceof HTMLSelectElement)))) {
    return element.value;
  } else if ((!(!(element instanceof HTMLButtonElement)))) {
    return element.value;
  } else if ((!(!(element instanceof HTMLOptionElement)))) {
    return element.value;
  } else if (this.nG(element)) {
    var x = element.value;
    new $c_Lcom_raquo_laminar_DomApi$$anon$2(this);
    return ((x === (void 0)) ? (void 0) : (((typeof x) === "string") ? x : (void 0)));
  } else {
    return (void 0);
  }
});
$p.pH = (function(element, initial) {
  var initial$tailLocal1 = initial;
  var element$tailLocal1 = element;
  while (true) {
    if ((element$tailLocal1 === null)) {
      return initial$tailLocal1;
    }
    var element$tailLocal1$tmp1 = element$tailLocal1.parentNode;
    var initial$tailLocal1$tmp1 = new $c_sci_$colon$colon(this.nj(element$tailLocal1), initial$tailLocal1);
    element$tailLocal1 = element$tailLocal1$tmp1;
    initial$tailLocal1 = initial$tailLocal1$tmp1;
  }
});
$p.nj = (function(node) {
  if ((!(!(node instanceof HTMLElement)))) {
    var id = node.id;
    if (($m_sc_StringOps$(), (id !== ""))) {
      var suffixStr = ("#" + id);
    } else {
      var classes = node.className;
      var suffixStr = (($m_sc_StringOps$(), (classes !== "")) ? ("." + classes.replace(this.ko, ".")) : "");
    }
    return (node.tagName.toLowerCase() + suffixStr);
  } else {
    return node.nodeName;
  }
});
$p.pG = (function(node) {
  return ((!(!(node instanceof Element))) ? node.outerHTML : ((!(!(node instanceof Text))) ? (("Text(" + node.textContent) + ")") : ((!(!(node instanceof Comment))) ? (("Comment(" + node.textContent) + ")") : ((node === null) ? "<null>" : (("OtherNode(" + $dp_toString__T(node)) + ")")))));
});
var $d_Lcom_raquo_laminar_DomApi$ = new $TypeData().i($c_Lcom_raquo_laminar_DomApi$, "com.raquo.laminar.DomApi$", ({
  de: 1
}));
var $n_Lcom_raquo_laminar_DomApi$;
function $m_Lcom_raquo_laminar_DomApi$() {
  if ((!$n_Lcom_raquo_laminar_DomApi$)) {
    $n_Lcom_raquo_laminar_DomApi$ = new $c_Lcom_raquo_laminar_DomApi$();
  }
  return $n_Lcom_raquo_laminar_DomApi$;
}
/** @constructor */
function $c_Lcom_raquo_laminar_Seq(seq, scalaArray, jsArray) {
  this.hG = null;
  this.kp = null;
  this.hF = null;
  this.hG = seq;
  this.kp = scalaArray;
  this.hF = jsArray;
}
$p = $c_Lcom_raquo_laminar_Seq.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_Seq;
/** @constructor */
function $h_Lcom_raquo_laminar_Seq() {
}
$h_Lcom_raquo_laminar_Seq.prototype = $p;
$p.bm = (function(f) {
  if ((this.hG !== null)) {
    this.hG.bm(f);
  } else if ((this.hF !== null)) {
    $m_Lcom_raquo_ew_JsArray$RichJsArray$().pY(this.hF, $m_sjs_js_Any$().nA(f));
  } else {
    $m_sc_ArrayOps$().q0(this.kp, f);
  }
});
var $d_Lcom_raquo_laminar_Seq = new $TypeData().i($c_Lcom_raquo_laminar_Seq, "com.raquo.laminar.Seq", ({
  dg: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_Seq$() {
  $n_Lcom_raquo_laminar_Seq$ = this;
  $m_sci_Nil$();
}
$p = $c_Lcom_raquo_laminar_Seq$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_Seq$;
/** @constructor */
function $h_Lcom_raquo_laminar_Seq$() {
}
$h_Lcom_raquo_laminar_Seq$.prototype = $p;
var $d_Lcom_raquo_laminar_Seq$ = new $TypeData().i($c_Lcom_raquo_laminar_Seq$, "com.raquo.laminar.Seq$", ({
  dh: 1
}));
var $n_Lcom_raquo_laminar_Seq$;
function $m_Lcom_raquo_laminar_Seq$() {
  if ((!$n_Lcom_raquo_laminar_Seq$)) {
    $n_Lcom_raquo_laminar_Seq$ = new $c_Lcom_raquo_laminar_Seq$();
  }
  return $n_Lcom_raquo_laminar_Seq$;
}
function $f_Lcom_raquo_laminar_api_AirstreamAliases__$init$__V($thiz) {
  $m_Lcom_raquo_airstream_core_Observer$();
  $m_Lcom_raquo_airstream_core_AirstreamError$();
  $thiz.dK = $m_Lcom_raquo_airstream_state_Var$();
}
function $f_Lcom_raquo_laminar_api_LaminarAliases__$init$__V($thiz) {
  $thiz.os = $m_Lcom_raquo_laminar_modifiers_Modifier$();
}
function $f_Lcom_raquo_laminar_api_MountHooks__$init$__V($thiz) {
  $f_Lcom_raquo_laminar_api_MountHooks__onMountCallback__F1__Lcom_raquo_laminar_modifiers_Modifier($thiz, new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((_$1) => {
    _$1.ly.b5.focus();
  })));
}
function $f_Lcom_raquo_laminar_api_MountHooks__onMountCallback__F1__Lcom_raquo_laminar_modifiers_Modifier($thiz, fn) {
  return new $c_Lcom_raquo_laminar_modifiers_Modifier$$anon$2(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((element) => {
    var ignoreNextActivation = new $c_sr_BooleanRef((!element.c4.bz.c()));
    var activate = new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((c) => {
      if (ignoreNextActivation.gP) {
        var ev$5 = false;
        ignoreNextActivation.gP = ev$5;
      } else {
        fn.b(c);
      }
    }));
    $m_Lcom_raquo_airstream_ownership_DynamicSubscription$().og(element.c4, new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((element$2) => ((owner) => {
      activate.b(new $c_Lcom_raquo_laminar_lifecycle_MountContext(element$2, owner));
    }))(element)), false);
  })), $m_Lcom_raquo_laminar_modifiers_Modifier$());
}
/** @constructor */
function $c_Lcom_raquo_laminar_codecs_package$() {
  this.f8 = null;
  this.hH = null;
  $n_Lcom_raquo_laminar_codecs_package$ = this;
  this.f8 = new $c_Lcom_raquo_laminar_codecs_package$$anon$2($m_Lcom_raquo_laminar_codecs_package$());
  new $c_Lcom_raquo_laminar_codecs_package$$anon$2($m_Lcom_raquo_laminar_codecs_package$());
  this.hH = new $c_Lcom_raquo_laminar_codecs_package$$anon$2($m_Lcom_raquo_laminar_codecs_package$());
}
$p = $c_Lcom_raquo_laminar_codecs_package$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_codecs_package$;
/** @constructor */
function $h_Lcom_raquo_laminar_codecs_package$() {
}
$h_Lcom_raquo_laminar_codecs_package$.prototype = $p;
var $d_Lcom_raquo_laminar_codecs_package$ = new $TypeData().i($c_Lcom_raquo_laminar_codecs_package$, "com.raquo.laminar.codecs.package$", ({
  ds: 1
}));
var $n_Lcom_raquo_laminar_codecs_package$;
function $m_Lcom_raquo_laminar_codecs_package$() {
  if ((!$n_Lcom_raquo_laminar_codecs_package$)) {
    $n_Lcom_raquo_laminar_codecs_package$ = new $c_Lcom_raquo_laminar_codecs_package$();
  }
  return $n_Lcom_raquo_laminar_codecs_package$;
}
function $f_Lcom_raquo_laminar_defs_complex_ComplexHtmlKeys__$init$__V($thiz) {
  $thiz.kB = $f_Lcom_raquo_laminar_defs_complex_ComplexHtmlKeys__stringCompositeHtmlAttr__T__T__Lcom_raquo_laminar_keys_CompositeKey($thiz, "class", " ");
  $thiz.dL = $thiz.kB;
}
function $f_Lcom_raquo_laminar_defs_complex_ComplexHtmlKeys__stringCompositeHtmlAttr__T__T__Lcom_raquo_laminar_keys_CompositeKey($thiz, name, separator) {
  var attr = new $c_Lcom_raquo_laminar_keys_HtmlAttr(name, $m_Lcom_raquo_laminar_codecs_package$().f8);
  return new $c_Lcom_raquo_laminar_keys_CompositeKey(attr.fa, new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((el) => {
    var x = $m_Lcom_raquo_laminar_DomApi$().q9(el, attr);
    return ((x === (void 0)) ? "" : x);
  })), new $c_sjsr_AnonFunction2_$$Lambda$770e9b86e03b055b1d78d82135c9f39ea48d32d7(((el$2, value) => {
    $m_Lcom_raquo_laminar_DomApi$().ra(el$2, attr, value);
  })), separator);
}
function $f_Lcom_raquo_laminar_defs_complex_ComplexSvgKeys__$init$__V($thiz) {
  $thiz.or = $f_Lcom_raquo_laminar_defs_complex_ComplexSvgKeys__stringCompositeSvgAttr__T__T__Lcom_raquo_laminar_keys_CompositeKey($thiz, "class", " ");
}
function $f_Lcom_raquo_laminar_defs_complex_ComplexSvgKeys__stringCompositeSvgAttr__T__T__Lcom_raquo_laminar_keys_CompositeKey($thiz, name, separator) {
  var attr = new $c_Lcom_raquo_laminar_keys_SvgAttr(name, $m_Lcom_raquo_laminar_codecs_package$().f8, $m_s_None$());
  return new $c_Lcom_raquo_laminar_keys_CompositeKey(attr.gx, new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((el) => {
    var x = $m_Lcom_raquo_laminar_DomApi$().qd(el, attr);
    return ((x === (void 0)) ? "" : x);
  })), new $c_sjsr_AnonFunction2_$$Lambda$770e9b86e03b055b1d78d82135c9f39ea48d32d7(((el$2, value) => {
    $m_Lcom_raquo_laminar_DomApi$().rd(el$2, attr, value);
  })), separator);
}
/** @constructor */
function $c_Lcom_raquo_laminar_inputs_InputController$() {
  this.lr = null;
  $n_Lcom_raquo_laminar_inputs_InputController$ = this;
  $m_Lcom_raquo_laminar_api_package$().o.hn();
  $m_Lcom_raquo_ew_JsArray$().bb($m_sr_ScalaRunTime$().b4(new ($d_Lcom_raquo_laminar_keys_EventProp.r().C)([$m_Lcom_raquo_laminar_api_package$().o.he()])));
  $m_Lcom_raquo_laminar_api_package$().o.hn();
  $m_Lcom_raquo_ew_JsArray$().bb($m_sr_ScalaRunTime$().b4(new ($d_Lcom_raquo_laminar_keys_EventProp.r().C)([$m_Lcom_raquo_laminar_api_package$().o.he(), $m_Lcom_raquo_laminar_api_package$().o.nV()])));
  $m_Lcom_raquo_laminar_api_package$().o.pq();
  $m_Lcom_raquo_ew_JsArray$().bb($m_sr_ScalaRunTime$().b4(new ($d_Lcom_raquo_laminar_keys_EventProp.r().C)([$m_Lcom_raquo_laminar_api_package$().o.he(), $m_Lcom_raquo_laminar_api_package$().o.nW()])));
  this.lr = $m_Lcom_raquo_ew_JsArray$().bb($m_sr_ScalaRunTime$().b4(new ($d_T.r().C)(["value", "checked"])));
}
$p = $c_Lcom_raquo_laminar_inputs_InputController$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_inputs_InputController$;
/** @constructor */
function $h_Lcom_raquo_laminar_inputs_InputController$() {
}
$h_Lcom_raquo_laminar_inputs_InputController$.prototype = $p;
var $d_Lcom_raquo_laminar_inputs_InputController$ = new $TypeData().i($c_Lcom_raquo_laminar_inputs_InputController$, "com.raquo.laminar.inputs.InputController$", ({
  dD: 1
}));
var $n_Lcom_raquo_laminar_inputs_InputController$;
function $m_Lcom_raquo_laminar_inputs_InputController$() {
  if ((!$n_Lcom_raquo_laminar_inputs_InputController$)) {
    $n_Lcom_raquo_laminar_inputs_InputController$ = new $c_Lcom_raquo_laminar_inputs_InputController$();
  }
  return $n_Lcom_raquo_laminar_inputs_InputController$;
}
/** @constructor */
function $c_Lcom_raquo_laminar_inserters_ChildInserter$() {
}
$p = $c_Lcom_raquo_laminar_inserters_ChildInserter$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_inserters_ChildInserter$;
/** @constructor */
function $h_Lcom_raquo_laminar_inserters_ChildInserter$() {
}
$h_Lcom_raquo_laminar_inserters_ChildInserter$.prototype = $p;
$p.p8 = (function(childSource, renderable, initialHooks) {
  return new $c_Lcom_raquo_laminar_inserters_DynamicInserter($m_s_None$(), true, new $c_sjsr_AnonFunction3_$$Lambda$73f37e31ba038fe839c174212837da323f140c96(((ctx, owner, hooks) => {
    if ((!ctx.cA)) {
      ctx.h5();
    }
    return $f_Lcom_raquo_airstream_core_BaseObservable__foreach__F1__Lcom_raquo_airstream_ownership_Owner__Lcom_raquo_airstream_ownership_Subscription(childSource, new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((ctx$2, maybeLastSeenChild) => ((newComponent) => {
      this.ro(maybeLastSeenChild.R, newComponent, ctx$2, hooks);
      var ev$3 = newComponent;
      maybeLastSeenChild.R = ev$3;
      ev$3 = null;
    }))(ctx, new $c_sr_ObjectRef((void 0)))), owner);
  })), initialHooks);
});
$p.ro = (function(maybeLastSeenChild, newChildNode, ctx, hooks) {
  if ((!ctx.cA)) {
    ctx.h5();
  }
  var elem = ctx.cy;
  var elem$1 = 0;
  elem$1 = elem;
  var x$1 = (((maybeLastSeenChild === (void 0)) || $m_sr_BoxesRunTime$().j(maybeLastSeenChild.I(), ctx.cz.I().nextSibling)) ? maybeLastSeenChild : (void 0));
  if ((x$1 === (void 0))) {
    $m_Lcom_raquo_laminar_nodes_ParentNode$().ha(ctx.d2, newChildNode, ctx.cz, hooks);
  } else if (($m_Lcom_raquo_laminar_nodes_ParentNode$().o5(ctx.d2, x$1, newChildNode, hooks) || (x$1 === newChildNode))) {
    var ev$4 = ((elem$1 - 1) | 0);
    elem$1 = ev$4;
  }
  ctx.o4(newChildNode);
  ctx.ce.clear();
  ctx.ce.set(newChildNode.I(), newChildNode);
  ctx.cy = 1;
});
var $d_Lcom_raquo_laminar_inserters_ChildInserter$ = new $TypeData().i($c_Lcom_raquo_laminar_inserters_ChildInserter$, "com.raquo.laminar.inserters.ChildInserter$", ({
  dE: 1
}));
var $n_Lcom_raquo_laminar_inserters_ChildInserter$;
function $m_Lcom_raquo_laminar_inserters_ChildInserter$() {
  if ((!$n_Lcom_raquo_laminar_inserters_ChildInserter$)) {
    $n_Lcom_raquo_laminar_inserters_ChildInserter$ = new $c_Lcom_raquo_laminar_inserters_ChildInserter$();
  }
  return $n_Lcom_raquo_laminar_inserters_ChildInserter$;
}
/** @constructor */
function $c_Lcom_raquo_laminar_inserters_ChildTextInserter$() {
}
$p = $c_Lcom_raquo_laminar_inserters_ChildTextInserter$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_inserters_ChildTextInserter$;
/** @constructor */
function $h_Lcom_raquo_laminar_inserters_ChildTextInserter$() {
}
$h_Lcom_raquo_laminar_inserters_ChildTextInserter$.prototype = $p;
$p.pa = (function(textSource, renderable) {
  return new $c_Lcom_raquo_laminar_inserters_DynamicInserter($m_s_None$(), false, new $c_sjsr_AnonFunction3_$$Lambda$73f37e31ba038fe839c174212837da323f140c96(((ctx, owner, _$1) => $f_Lcom_raquo_airstream_core_BaseObservable__foreach__F1__Lcom_raquo_airstream_ownership_Owner__Lcom_raquo_airstream_ownership_Subscription(textSource, new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((ctx$2, maybeTextNode) => ((newValue) => {
    var x = maybeTextNode.R;
    if ((x === (void 0))) {
      var newTextNode = new $c_Lcom_raquo_laminar_nodes_TextNode(renderable.iK(newValue));
      this.rq(newTextNode, ctx$2);
      var ev$2 = newTextNode;
      maybeTextNode.R = ev$2;
      ev$2 = null;
    } else {
      x.gz.textContent = renderable.iK(newValue);
    }
  }))(ctx, new $c_sr_ObjectRef((void 0)))), owner))), (void 0));
});
$p.rq = (function(newTextNode, ctx) {
  $m_Lcom_raquo_laminar_nodes_ParentNode$().o5(ctx.d2, ctx.cz, newTextNode, (void 0));
  ctx.cz = newTextNode;
  if (ctx.cA) {
    ctx.cA = false;
    ctx.o4(newTextNode);
    ctx.ce.clear();
    ctx.cy = 0;
  }
});
var $d_Lcom_raquo_laminar_inserters_ChildTextInserter$ = new $TypeData().i($c_Lcom_raquo_laminar_inserters_ChildTextInserter$, "com.raquo.laminar.inserters.ChildTextInserter$", ({
  dF: 1
}));
var $n_Lcom_raquo_laminar_inserters_ChildTextInserter$;
function $m_Lcom_raquo_laminar_inserters_ChildTextInserter$() {
  if ((!$n_Lcom_raquo_laminar_inserters_ChildTextInserter$)) {
    $n_Lcom_raquo_laminar_inserters_ChildTextInserter$ = new $c_Lcom_raquo_laminar_inserters_ChildTextInserter$();
  }
  return $n_Lcom_raquo_laminar_inserters_ChildTextInserter$;
}
function $p_Lcom_raquo_laminar_inserters_ChildrenInserter$__updateChildren__Lcom_raquo_ew_JsMap__Lcom_raquo_laminar_Seq__Lcom_raquo_ew_JsMap__Lcom_raquo_laminar_nodes_ReactiveElement__Lcom_raquo_laminar_nodes_ChildNode__I__O__I($thiz, prevChildren, nextChildren, nextChildrenMap, parentNode, sentinelNode, prevChildrenCount, hooks) {
  var index = new $c_sr_IntRef(0);
  var currentChildrenCount = new $c_sr_IntRef(prevChildrenCount);
  var prevChildRef = new $c_sr_ObjectRef(sentinelNode.I().nextSibling);
  var lastIndexChild = new $c_sr_ObjectRef(sentinelNode);
  nextChildren.bm(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((nextChild) => {
    if ((currentChildrenCount.ab <= index.ab)) {
      $m_Lcom_raquo_laminar_nodes_ParentNode$().ha(parentNode, nextChild, lastIndexChild.R, hooks);
      var ev$2 = nextChild.I();
      prevChildRef.R = ev$2;
      ev$2 = null;
      var ev$3 = ((1 + currentChildrenCount.ab) | 0);
      currentChildrenCount.ab = ev$3;
    } else if ((!$m_sr_BoxesRunTime$().j(nextChild.I(), prevChildRef.R))) {
      if ((!(!(!prevChildren.has(nextChild.I()))))) {
        $m_Lcom_raquo_laminar_nodes_ParentNode$().ha(parentNode, nextChild, lastIndexChild.R, hooks);
        var ev$4 = nextChild.I();
        prevChildRef.R = ev$4;
        ev$4 = null;
        var ev$5 = ((1 + currentChildrenCount.ab) | 0);
        currentChildrenCount.ab = ev$5;
      } else {
        while (((!$m_sr_BoxesRunTime$().j(nextChild.I(), prevChildRef.R)) && (!$p_Lcom_raquo_laminar_inserters_ChildrenInserter$__containsRef__Lcom_raquo_ew_JsMap__Lorg_scalajs_dom_Node__Z($thiz, nextChildrenMap, prevChildRef.R)))) {
          var nextPrevChildRef = prevChildRef.R.nextSibling;
          $m_Lcom_raquo_laminar_nodes_ParentNode$().jr(parentNode, $p_Lcom_raquo_laminar_inserters_ChildrenInserter$__prevChildFromRef__Lcom_raquo_ew_JsMap__Lorg_scalajs_dom_Node__Lcom_raquo_laminar_nodes_ChildNode($thiz, prevChildren, prevChildRef.R));
          var ev$6 = nextPrevChildRef;
          prevChildRef.R = ev$6;
          ev$6 = null;
          var ev$7 = ((currentChildrenCount.ab - 1) | 0);
          currentChildrenCount.ab = ev$7;
        }
        if ((!$m_sr_BoxesRunTime$().j(nextChild.I(), prevChildRef.R))) {
          $m_Lcom_raquo_laminar_nodes_ParentNode$().ha(parentNode, nextChild, lastIndexChild.R, hooks);
          var ev$8 = nextChild.I();
          prevChildRef.R = ev$8;
          ev$8 = null;
        }
      }
    }
    if ((prevChildRef.R.nextSibling === null)) {
      var ev$9 = ((1 + index.ab) | 0);
      currentChildrenCount.ab = ev$9;
    } else {
      var ev$10 = prevChildRef.R.nextSibling;
      prevChildRef.R = ev$10;
      ev$10 = null;
    }
    var ev$11 = nextChild;
    lastIndexChild.R = ev$11;
    ev$11 = null;
    var ev$12 = ((1 + index.ab) | 0);
    index.ab = ev$12;
  })));
  while ((index.ab < currentChildrenCount.ab)) {
    var nextPrevChildRef$1 = prevChildRef.R.nextSibling;
    $m_Lcom_raquo_laminar_nodes_ParentNode$().jr(parentNode, $p_Lcom_raquo_laminar_inserters_ChildrenInserter$__prevChildFromRef__Lcom_raquo_ew_JsMap__Lorg_scalajs_dom_Node__Lcom_raquo_laminar_nodes_ChildNode($thiz, prevChildren, prevChildRef.R));
    var ev$13 = nextPrevChildRef$1;
    prevChildRef.R = ev$13;
    ev$13 = null;
    var ev$14 = ((currentChildrenCount.ab - 1) | 0);
    currentChildrenCount.ab = ev$14;
  }
  return currentChildrenCount.ab;
}
function $p_Lcom_raquo_laminar_inserters_ChildrenInserter$__containsRef__Lcom_raquo_ew_JsMap__Lorg_scalajs_dom_Node__Z($thiz, nextChildrenMap, ref) {
  return (!(!nextChildrenMap.has(ref)));
}
function $p_Lcom_raquo_laminar_inserters_ChildrenInserter$__prevChildFromRef__Lcom_raquo_ew_JsMap__Lorg_scalajs_dom_Node__Lcom_raquo_laminar_nodes_ChildNode($thiz, prevChildren, ref) {
  var x = prevChildren.get(ref);
  if ((x === (void 0))) {
    throw $ct_jl_Exception__T__(new $c_jl_Exception(), ("prevChildFromRef[children]: not found for " + ref));
  }
  return x;
}
/** @constructor */
function $c_Lcom_raquo_laminar_inserters_ChildrenInserter$() {
}
$p = $c_Lcom_raquo_laminar_inserters_ChildrenInserter$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_inserters_ChildrenInserter$;
/** @constructor */
function $h_Lcom_raquo_laminar_inserters_ChildrenInserter$() {
}
$h_Lcom_raquo_laminar_inserters_ChildrenInserter$.prototype = $p;
$p.p9 = (function(childrenSource, renderableSeq, renderableNode, initialHooks) {
  return new $c_Lcom_raquo_laminar_inserters_DynamicInserter($m_s_None$(), true, new $c_sjsr_AnonFunction3_$$Lambda$73f37e31ba038fe839c174212837da323f140c96(((ctx, owner, hooks) => {
    if ((!ctx.cA)) {
      ctx.h5();
    }
    return $f_Lcom_raquo_airstream_core_BaseObservable__foreach__F1__Lcom_raquo_airstream_ownership_Owner__Lcom_raquo_airstream_ownership_Subscription(childrenSource, new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((ctx$2) => ((components) => {
      this.rp(($m_Lcom_raquo_laminar_Seq$(), new $c_Lcom_raquo_laminar_Seq(components, null, null)), ctx$2, hooks);
    }))(ctx)), owner);
  })), initialHooks);
});
$p.rp = (function(newChildren, ctx, hooks) {
  if ((!ctx.cA)) {
    ctx.h5();
  }
  var newChildrenMap = $m_Lcom_raquo_laminar_inserters_InsertContext$().qI(newChildren);
  ctx.cy = $p_Lcom_raquo_laminar_inserters_ChildrenInserter$__updateChildren__Lcom_raquo_ew_JsMap__Lcom_raquo_laminar_Seq__Lcom_raquo_ew_JsMap__Lcom_raquo_laminar_nodes_ReactiveElement__Lcom_raquo_laminar_nodes_ChildNode__I__O__I(this, ctx.ce, newChildren, newChildrenMap, ctx.d2, ctx.cz, ctx.cy, hooks);
  ctx.ce = newChildrenMap;
});
var $d_Lcom_raquo_laminar_inserters_ChildrenInserter$ = new $TypeData().i($c_Lcom_raquo_laminar_inserters_ChildrenInserter$, "com.raquo.laminar.inserters.ChildrenInserter$", ({
  dG: 1
}));
var $n_Lcom_raquo_laminar_inserters_ChildrenInserter$;
function $m_Lcom_raquo_laminar_inserters_ChildrenInserter$() {
  if ((!$n_Lcom_raquo_laminar_inserters_ChildrenInserter$)) {
    $n_Lcom_raquo_laminar_inserters_ChildrenInserter$ = new $c_Lcom_raquo_laminar_inserters_ChildrenInserter$();
  }
  return $n_Lcom_raquo_laminar_inserters_ChildrenInserter$;
}
/** @constructor */
function $c_Lcom_raquo_laminar_inserters_InsertContext(parentNode, sentinelNode, strictMode, extraNodeCount, extraNodesMap) {
  this.d2 = null;
  this.cz = null;
  this.cA = false;
  this.cy = 0;
  this.ce = null;
  this.d2 = parentNode;
  this.cz = sentinelNode;
  this.cA = strictMode;
  this.cy = extraNodeCount;
  this.ce = extraNodesMap;
}
$p = $c_Lcom_raquo_laminar_inserters_InsertContext.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_inserters_InsertContext;
/** @constructor */
function $h_Lcom_raquo_laminar_inserters_InsertContext() {
}
$h_Lcom_raquo_laminar_inserters_InsertContext.prototype = $p;
$p.h5 = (function() {
  if ((this.cA || (this.cy !== 0))) {
    throw $ct_jl_Exception__T__(new $c_jl_Exception(), ("forceSetStrictMode invoked when not allowed, inside parent = " + $m_Lcom_raquo_laminar_DomApi$().pG(this.d2.b5)));
  }
  if ((this.ce === null)) {
    this.ce = new Map();
  }
  if ((!(!(!(this.cz.I() instanceof Comment))))) {
    var contentNode = this.cz;
    var newSentinelNode = new $c_Lcom_raquo_laminar_nodes_CommentNode("");
    $m_Lcom_raquo_laminar_DomApi$().qp(this.d2.b5, newSentinelNode.hW, contentNode.I());
    this.cz = newSentinelNode;
    this.cy = 1;
    this.ce.set(contentNode.I(), contentNode);
  }
  this.cA = true;
});
$p.o4 = (function(after) {
  var elem = this.cy;
  var elem$1 = 0;
  elem$1 = elem;
  while ((elem$1 > 0)) {
    var prevChildRef = after.I().nextSibling;
    if ((prevChildRef === null)) {
      var ev$3 = 0;
      elem$1 = ev$3;
    } else {
      var maybePrevChild = this.ce.get(prevChildRef);
      if ((maybePrevChild === (void 0))) {
        var ev$4 = 0;
        elem$1 = ev$4;
      } else if ((maybePrevChild !== (void 0))) {
        $m_Lcom_raquo_laminar_nodes_ParentNode$().jr(this.d2, maybePrevChild);
        var ev$5 = ((elem$1 - 1) | 0);
        elem$1 = ev$5;
      }
    }
  }
});
var $d_Lcom_raquo_laminar_inserters_InsertContext = new $TypeData().i($c_Lcom_raquo_laminar_inserters_InsertContext, "com.raquo.laminar.inserters.InsertContext", ({
  dJ: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_inserters_InsertContext$() {
}
$p = $c_Lcom_raquo_laminar_inserters_InsertContext$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_inserters_InsertContext$;
/** @constructor */
function $h_Lcom_raquo_laminar_inserters_InsertContext$() {
}
$h_Lcom_raquo_laminar_inserters_InsertContext$.prototype = $p;
$p.r3 = (function(parentNode, strictMode, hooks) {
  var sentinelNode = new $c_Lcom_raquo_laminar_nodes_CommentNode("");
  $m_Lcom_raquo_laminar_nodes_ParentNode$().eL(parentNode, sentinelNode, hooks);
  return this.rF(parentNode, sentinelNode, strictMode);
});
$p.rF = (function(parentNode, sentinelNode, strictMode) {
  return new $c_Lcom_raquo_laminar_inserters_InsertContext(parentNode, sentinelNode, strictMode, 0, (strictMode ? new Map() : null));
});
$p.qI = (function(nodes) {
  var acc = new Map();
  nodes.bm(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((node) => {
    acc.set(node.I(), node);
  })));
  return acc;
});
var $d_Lcom_raquo_laminar_inserters_InsertContext$ = new $TypeData().i($c_Lcom_raquo_laminar_inserters_InsertContext$, "com.raquo.laminar.inserters.InsertContext$", ({
  dK: 1
}));
var $n_Lcom_raquo_laminar_inserters_InsertContext$;
function $m_Lcom_raquo_laminar_inserters_InsertContext$() {
  if ((!$n_Lcom_raquo_laminar_inserters_InsertContext$)) {
    $n_Lcom_raquo_laminar_inserters_InsertContext$ = new $c_Lcom_raquo_laminar_inserters_InsertContext$();
  }
  return $n_Lcom_raquo_laminar_inserters_InsertContext$;
}
/** @constructor */
function $c_Lcom_raquo_laminar_keys_CompositeKey$() {
}
$p = $c_Lcom_raquo_laminar_keys_CompositeKey$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_keys_CompositeKey$;
/** @constructor */
function $h_Lcom_raquo_laminar_keys_CompositeKey$() {
}
$h_Lcom_raquo_laminar_keys_CompositeKey$.prototype = $p;
$p.nT = (function(items, separator) {
  if ((items === "")) {
    return $m_sci_Nil$();
  } else {
    var this$10 = $ct_sjs_js_WrappedArray__sjs_js_Array__(new $c_sjs_js_WrappedArray(), items.split(separator).filter(((_$1) => {
      $m_sc_StringOps$();
      return (_$1 !== "");
    })));
    $m_sci_List$();
    return $m_sci_Nil$().eU(this$10);
  }
});
var $d_Lcom_raquo_laminar_keys_CompositeKey$ = new $TypeData().i($c_Lcom_raquo_laminar_keys_CompositeKey$, "com.raquo.laminar.keys.CompositeKey$", ({
  dN: 1
}));
var $n_Lcom_raquo_laminar_keys_CompositeKey$;
function $m_Lcom_raquo_laminar_keys_CompositeKey$() {
  if ((!$n_Lcom_raquo_laminar_keys_CompositeKey$)) {
    $n_Lcom_raquo_laminar_keys_CompositeKey$ = new $c_Lcom_raquo_laminar_keys_CompositeKey$();
  }
  return $n_Lcom_raquo_laminar_keys_CompositeKey$;
}
/** @constructor */
function $c_Lcom_raquo_laminar_keys_EventProcessor(eventProp, shouldUseCapture, shouldBePassive, processor) {
  this.ei = null;
  this.gw = false;
  this.hL = false;
  this.gv = null;
  this.ei = eventProp;
  this.gw = shouldUseCapture;
  this.hL = shouldBePassive;
  this.gv = processor;
}
$p = $c_Lcom_raquo_laminar_keys_EventProcessor.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_keys_EventProcessor;
/** @constructor */
function $h_Lcom_raquo_laminar_keys_EventProcessor() {
}
$h_Lcom_raquo_laminar_keys_EventProcessor.prototype = $p;
$p.nP = (function() {
  var newProcessor = new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((ev) => {
    var this$2 = this.gv.b(ev);
    if (this$2.c()) {
      return $m_s_None$();
    } else {
      this$2.s();
      var x = $m_Lcom_raquo_laminar_DomApi$().qf(ev.target);
      return new $c_s_Some(((x === (void 0)) ? "" : x));
    }
  }));
  return new $c_Lcom_raquo_laminar_keys_EventProcessor(this.ei, this.gw, this.hL, newProcessor);
});
var $d_Lcom_raquo_laminar_keys_EventProcessor = new $TypeData().i($c_Lcom_raquo_laminar_keys_EventProcessor, "com.raquo.laminar.keys.EventProcessor", ({
  dR: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_keys_EventProcessor$() {
}
$p = $c_Lcom_raquo_laminar_keys_EventProcessor$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_keys_EventProcessor$;
/** @constructor */
function $h_Lcom_raquo_laminar_keys_EventProcessor$() {
}
$h_Lcom_raquo_laminar_keys_EventProcessor$.prototype = $p;
$p.h4 = (function(eventProp, shouldUseCapture, shouldBePassive) {
  return new $c_Lcom_raquo_laminar_keys_EventProcessor(eventProp, shouldUseCapture, shouldBePassive, new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((_$14) => new $c_s_Some(_$14))));
});
var $d_Lcom_raquo_laminar_keys_EventProcessor$ = new $TypeData().i($c_Lcom_raquo_laminar_keys_EventProcessor$, "com.raquo.laminar.keys.EventProcessor$", ({
  dS: 1
}));
var $n_Lcom_raquo_laminar_keys_EventProcessor$;
function $m_Lcom_raquo_laminar_keys_EventProcessor$() {
  if ((!$n_Lcom_raquo_laminar_keys_EventProcessor$)) {
    $n_Lcom_raquo_laminar_keys_EventProcessor$ = new $c_Lcom_raquo_laminar_keys_EventProcessor$();
  }
  return $n_Lcom_raquo_laminar_keys_EventProcessor$;
}
/** @constructor */
function $c_Lcom_raquo_laminar_keys_Key() {
}
$p = $c_Lcom_raquo_laminar_keys_Key.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_keys_Key;
/** @constructor */
function $h_Lcom_raquo_laminar_keys_Key() {
}
$h_Lcom_raquo_laminar_keys_Key.prototype = $p;
/** @constructor */
function $c_Lcom_raquo_laminar_keys_SvgAttr$() {
  this.ov = null;
  this.ow = null;
  this.ox = null;
  this.oy = null;
  this.ov = "http://www.w3.org/2000/svg";
  this.ow = "http://www.w3.org/1999/xlink";
  this.ox = "http://www.w3.org/XML/1998/namespace";
  this.oy = "http://www.w3.org/2000/xmlns/";
}
$p = $c_Lcom_raquo_laminar_keys_SvgAttr$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_keys_SvgAttr$;
/** @constructor */
function $h_Lcom_raquo_laminar_keys_SvgAttr$() {
}
$h_Lcom_raquo_laminar_keys_SvgAttr$.prototype = $p;
$p.qD = (function(namespace) {
  switch (namespace) {
    case "svg": {
      return "http://www.w3.org/2000/svg";
      break;
    }
    case "xlink": {
      return "http://www.w3.org/1999/xlink";
      break;
    }
    case "xml": {
      return "http://www.w3.org/XML/1998/namespace";
      break;
    }
    case "xmlns": {
      return "http://www.w3.org/2000/xmlns/";
      break;
    }
    default: {
      throw new $c_s_MatchError(namespace);
    }
  }
});
var $d_Lcom_raquo_laminar_keys_SvgAttr$ = new $TypeData().i($c_Lcom_raquo_laminar_keys_SvgAttr$, "com.raquo.laminar.keys.SvgAttr$", ({
  dW: 1
}));
var $n_Lcom_raquo_laminar_keys_SvgAttr$;
function $m_Lcom_raquo_laminar_keys_SvgAttr$() {
  if ((!$n_Lcom_raquo_laminar_keys_SvgAttr$)) {
    $n_Lcom_raquo_laminar_keys_SvgAttr$ = new $c_Lcom_raquo_laminar_keys_SvgAttr$();
  }
  return $n_Lcom_raquo_laminar_keys_SvgAttr$;
}
/** @constructor */
function $c_Lcom_raquo_laminar_lifecycle_MountContext(thisNode, owner) {
  this.ly = null;
  this.hQ = null;
  this.ly = thisNode;
  this.hQ = owner;
}
$p = $c_Lcom_raquo_laminar_lifecycle_MountContext.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_lifecycle_MountContext;
/** @constructor */
function $h_Lcom_raquo_laminar_lifecycle_MountContext() {
}
$h_Lcom_raquo_laminar_lifecycle_MountContext.prototype = $p;
var $d_Lcom_raquo_laminar_lifecycle_MountContext = new $TypeData().i($c_Lcom_raquo_laminar_lifecycle_MountContext, "com.raquo.laminar.lifecycle.MountContext", ({
  dX: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_modifiers_Modifier$() {
  this.oz = null;
  $n_Lcom_raquo_laminar_modifiers_Modifier$ = this;
  this.oz = new $c_Lcom_raquo_laminar_modifiers_Modifier$$anon$1();
}
$p = $c_Lcom_raquo_laminar_modifiers_Modifier$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_modifiers_Modifier$;
/** @constructor */
function $h_Lcom_raquo_laminar_modifiers_Modifier$() {
}
$h_Lcom_raquo_laminar_modifiers_Modifier$.prototype = $p;
var $d_Lcom_raquo_laminar_modifiers_Modifier$ = new $TypeData().i($c_Lcom_raquo_laminar_modifiers_Modifier$, "com.raquo.laminar.modifiers.Modifier$", ({
  e2: 1
}));
var $n_Lcom_raquo_laminar_modifiers_Modifier$;
function $m_Lcom_raquo_laminar_modifiers_Modifier$() {
  if ((!$n_Lcom_raquo_laminar_modifiers_Modifier$)) {
    $n_Lcom_raquo_laminar_modifiers_Modifier$ = new $c_Lcom_raquo_laminar_modifiers_Modifier$();
  }
  return $n_Lcom_raquo_laminar_modifiers_Modifier$;
}
/** @constructor */
function $c_Lcom_raquo_laminar_modifiers_RenderableNode$() {
  this.hU = null;
  $n_Lcom_raquo_laminar_modifiers_RenderableNode$ = this;
  this.hU = new $c_Lcom_raquo_laminar_modifiers_RenderableNode$$anon$1();
}
$p = $c_Lcom_raquo_laminar_modifiers_RenderableNode$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_modifiers_RenderableNode$;
/** @constructor */
function $h_Lcom_raquo_laminar_modifiers_RenderableNode$() {
}
$h_Lcom_raquo_laminar_modifiers_RenderableNode$.prototype = $p;
var $d_Lcom_raquo_laminar_modifiers_RenderableNode$ = new $TypeData().i($c_Lcom_raquo_laminar_modifiers_RenderableNode$, "com.raquo.laminar.modifiers.RenderableNode$", ({
  e6: 1
}));
var $n_Lcom_raquo_laminar_modifiers_RenderableNode$;
function $m_Lcom_raquo_laminar_modifiers_RenderableNode$() {
  if ((!$n_Lcom_raquo_laminar_modifiers_RenderableNode$)) {
    $n_Lcom_raquo_laminar_modifiers_RenderableNode$ = new $c_Lcom_raquo_laminar_modifiers_RenderableNode$();
  }
  return $n_Lcom_raquo_laminar_modifiers_RenderableNode$;
}
/** @constructor */
function $c_Lcom_raquo_laminar_modifiers_RenderableText$() {
  this.br = null;
  $n_Lcom_raquo_laminar_modifiers_RenderableText$ = this;
  this.br = new $c_Lcom_raquo_laminar_modifiers_RenderableText$$anon$1(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((x) => x)), $m_Lcom_raquo_laminar_modifiers_RenderableText$());
  new $c_Lcom_raquo_laminar_modifiers_RenderableText$$anon$1(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((_$1) => ("" + (_$1 | 0)))), $m_Lcom_raquo_laminar_modifiers_RenderableText$());
  new $c_Lcom_raquo_laminar_modifiers_RenderableText$$anon$1(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((_$2) => ("" + (+_$2)))), $m_Lcom_raquo_laminar_modifiers_RenderableText$());
  new $c_Lcom_raquo_laminar_modifiers_RenderableText$$anon$1(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((_$3) => ("" + (!(!_$3))))), $m_Lcom_raquo_laminar_modifiers_RenderableText$());
  new $c_Lcom_raquo_laminar_modifiers_RenderableText$$anon$1(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((_$4) => _$4.rw())), $m_Lcom_raquo_laminar_modifiers_RenderableText$());
}
$p = $c_Lcom_raquo_laminar_modifiers_RenderableText$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_modifiers_RenderableText$;
/** @constructor */
function $h_Lcom_raquo_laminar_modifiers_RenderableText$() {
}
$h_Lcom_raquo_laminar_modifiers_RenderableText$.prototype = $p;
var $d_Lcom_raquo_laminar_modifiers_RenderableText$ = new $TypeData().i($c_Lcom_raquo_laminar_modifiers_RenderableText$, "com.raquo.laminar.modifiers.RenderableText$", ({
  eb: 1
}));
var $n_Lcom_raquo_laminar_modifiers_RenderableText$;
function $m_Lcom_raquo_laminar_modifiers_RenderableText$() {
  if ((!$n_Lcom_raquo_laminar_modifiers_RenderableText$)) {
    $n_Lcom_raquo_laminar_modifiers_RenderableText$ = new $c_Lcom_raquo_laminar_modifiers_RenderableText$();
  }
  return $n_Lcom_raquo_laminar_modifiers_RenderableText$;
}
/** @constructor */
function $c_Lcom_raquo_laminar_nodes_ParentNode$() {
}
$p = $c_Lcom_raquo_laminar_nodes_ParentNode$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_nodes_ParentNode$;
/** @constructor */
function $h_Lcom_raquo_laminar_nodes_ParentNode$() {
}
$h_Lcom_raquo_laminar_nodes_ParentNode$.prototype = $p;
$p.eL = (function(parent, child, hooks) {
  var nextParent = new $c_s_Some(parent);
  child.ec(nextParent);
  if ((hooks !== (void 0))) {
    hooks.o0(parent, child);
  }
  var appended = $m_Lcom_raquo_laminar_DomApi$().p7(parent.I(), child.I());
  if (appended) {
    child.e9(nextParent);
  }
  return appended;
});
$p.jr = (function(parent, child) {
  var removed = false;
  if ($m_sr_BoxesRunTime$().j(child.I().parentNode, parent.I())) {
    child.ec($m_s_None$());
    removed = $m_Lcom_raquo_laminar_DomApi$().qW(parent.I(), child.I());
    child.e9($m_s_None$());
  }
  return removed;
});
$p.ha = (function(parent, newChild, referenceChild, hooks) {
  var nextParent = new $c_s_Some(parent);
  newChild.ec(nextParent);
  if ((hooks !== (void 0))) {
    hooks.o0(parent, newChild);
  }
  var inserted = $m_Lcom_raquo_laminar_DomApi$().qo(parent.I(), newChild.I(), referenceChild.I());
  newChild.e9(nextParent);
  return inserted;
});
$p.o5 = (function(parent, oldChild, newChild, hooks) {
  var replaced = false;
  if ((oldChild !== newChild)) {
    if (oldChild.iM().bl(parent)) {
      var newChildNextParent = new $c_s_Some(parent);
      oldChild.ec($m_s_None$());
      newChild.ec(newChildNextParent);
      if ((hooks !== (void 0))) {
        hooks.o0(parent, newChild);
      }
      replaced = $m_Lcom_raquo_laminar_DomApi$().r1(parent.I(), newChild.I(), oldChild.I());
      if (replaced) {
        oldChild.e9($m_s_None$());
        newChild.e9(newChildNextParent);
      }
    }
  }
  return replaced;
});
var $d_Lcom_raquo_laminar_nodes_ParentNode$ = new $TypeData().i($c_Lcom_raquo_laminar_nodes_ParentNode$, "com.raquo.laminar.nodes.ParentNode$", ({
  ee: 1
}));
var $n_Lcom_raquo_laminar_nodes_ParentNode$;
function $m_Lcom_raquo_laminar_nodes_ParentNode$() {
  if ((!$n_Lcom_raquo_laminar_nodes_ParentNode$)) {
    $n_Lcom_raquo_laminar_nodes_ParentNode$ = new $c_Lcom_raquo_laminar_nodes_ParentNode$();
  }
  return $n_Lcom_raquo_laminar_nodes_ParentNode$;
}
/** @constructor */
function $c_Lcom_raquo_laminar_nodes_ReactiveElement$() {
}
$p = $c_Lcom_raquo_laminar_nodes_ReactiveElement$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_nodes_ReactiveElement$;
/** @constructor */
function $h_Lcom_raquo_laminar_nodes_ReactiveElement$() {
}
$h_Lcom_raquo_laminar_nodes_ReactiveElement$.prototype = $p;
$p.rE = (function(element, subscribe) {
  return $m_Lcom_raquo_airstream_ownership_DynamicSubscription$().gk(element.c4, new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((owner) => subscribe.b(new $c_Lcom_raquo_laminar_lifecycle_MountContext(element, owner)))), true);
});
var $d_Lcom_raquo_laminar_nodes_ReactiveElement$ = new $TypeData().i($c_Lcom_raquo_laminar_nodes_ReactiveElement$, "com.raquo.laminar.nodes.ReactiveElement$", ({
  eg: 1
}));
var $n_Lcom_raquo_laminar_nodes_ReactiveElement$;
function $m_Lcom_raquo_laminar_nodes_ReactiveElement$() {
  if ((!$n_Lcom_raquo_laminar_nodes_ReactiveElement$)) {
    $n_Lcom_raquo_laminar_nodes_ReactiveElement$ = new $c_Lcom_raquo_laminar_nodes_ReactiveElement$();
  }
  return $n_Lcom_raquo_laminar_nodes_ReactiveElement$;
}
/** @constructor */
function $c_Lcom_raquo_laminar_receivers_ChildReceiver$() {
  this.oA = null;
  $n_Lcom_raquo_laminar_receivers_ChildReceiver$ = this;
  this.oA = $m_Lcom_raquo_laminar_receivers_ChildTextReceiver$();
}
$p = $c_Lcom_raquo_laminar_receivers_ChildReceiver$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_receivers_ChildReceiver$;
/** @constructor */
function $h_Lcom_raquo_laminar_receivers_ChildReceiver$() {
}
$h_Lcom_raquo_laminar_receivers_ChildReceiver$.prototype = $p;
var $d_Lcom_raquo_laminar_receivers_ChildReceiver$ = new $TypeData().i($c_Lcom_raquo_laminar_receivers_ChildReceiver$, "com.raquo.laminar.receivers.ChildReceiver$", ({
  ek: 1
}));
var $n_Lcom_raquo_laminar_receivers_ChildReceiver$;
function $m_Lcom_raquo_laminar_receivers_ChildReceiver$() {
  if ((!$n_Lcom_raquo_laminar_receivers_ChildReceiver$)) {
    $n_Lcom_raquo_laminar_receivers_ChildReceiver$ = new $c_Lcom_raquo_laminar_receivers_ChildReceiver$();
  }
  return $n_Lcom_raquo_laminar_receivers_ChildReceiver$;
}
/** @constructor */
function $c_Lcom_raquo_laminar_receivers_ChildTextReceiver$() {
}
$p = $c_Lcom_raquo_laminar_receivers_ChildTextReceiver$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_receivers_ChildTextReceiver$;
/** @constructor */
function $h_Lcom_raquo_laminar_receivers_ChildTextReceiver$() {
}
$h_Lcom_raquo_laminar_receivers_ChildTextReceiver$.prototype = $p;
var $d_Lcom_raquo_laminar_receivers_ChildTextReceiver$ = new $TypeData().i($c_Lcom_raquo_laminar_receivers_ChildTextReceiver$, "com.raquo.laminar.receivers.ChildTextReceiver$", ({
  el: 1
}));
var $n_Lcom_raquo_laminar_receivers_ChildTextReceiver$;
function $m_Lcom_raquo_laminar_receivers_ChildTextReceiver$() {
  if ((!$n_Lcom_raquo_laminar_receivers_ChildTextReceiver$)) {
    $n_Lcom_raquo_laminar_receivers_ChildTextReceiver$ = new $c_Lcom_raquo_laminar_receivers_ChildTextReceiver$();
  }
  return $n_Lcom_raquo_laminar_receivers_ChildTextReceiver$;
}
/** @constructor */
function $c_Lcom_raquo_laminar_receivers_ChildrenReceiver$() {
}
$p = $c_Lcom_raquo_laminar_receivers_ChildrenReceiver$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_receivers_ChildrenReceiver$;
/** @constructor */
function $h_Lcom_raquo_laminar_receivers_ChildrenReceiver$() {
}
$h_Lcom_raquo_laminar_receivers_ChildrenReceiver$.prototype = $p;
var $d_Lcom_raquo_laminar_receivers_ChildrenReceiver$ = new $TypeData().i($c_Lcom_raquo_laminar_receivers_ChildrenReceiver$, "com.raquo.laminar.receivers.ChildrenReceiver$", ({
  em: 1
}));
var $n_Lcom_raquo_laminar_receivers_ChildrenReceiver$;
function $m_Lcom_raquo_laminar_receivers_ChildrenReceiver$() {
  if ((!$n_Lcom_raquo_laminar_receivers_ChildrenReceiver$)) {
    $n_Lcom_raquo_laminar_receivers_ChildrenReceiver$ = new $c_Lcom_raquo_laminar_receivers_ChildrenReceiver$();
  }
  return $n_Lcom_raquo_laminar_receivers_ChildrenReceiver$;
}
/** @constructor */
function $c_Ldpm_Data$() {
  this.lM = null;
  this.lN = false;
}
$p = $c_Ldpm_Data$.prototype = new $h_O();
$p.constructor = $c_Ldpm_Data$;
/** @constructor */
function $h_Ldpm_Data$() {
}
$h_Ldpm_Data$.prototype = $p;
$p.pj = (function() {
  if ((!this.lN)) {
    this.lM = new URL("data/", document.baseURI).href;
    this.lN = true;
  }
  return this.lM;
});
$p.oo = (function(path) {
  return (("" + this.pj()) + path);
});
var $d_Ldpm_Data$ = new $TypeData().i($c_Ldpm_Data$, "dpm.Data$", ({
  eq: 1
}));
var $n_Ldpm_Data$;
function $m_Ldpm_Data$() {
  if ((!$n_Ldpm_Data$)) {
    $n_Ldpm_Data$ = new $c_Ldpm_Data$();
  }
  return $n_Ldpm_Data$;
}
function $s_Ldpm_Main__main__AT__V(args) {
  $m_Ldpm_Main$().qy(args);
}
function $p_Ldpm_Main$__connection__s_concurrent_Future($thiz) {
  var x6 = $f_Lcom_raquo_airstream_core_WritableSignal__tryNow__s_util_Try($thiz.i3.c3).s();
  if ((x6 instanceof $c_s_Some)) {
    var con = x6.cC;
    return $m_s_concurrent_Future$().rj(con);
  }
  if (($m_s_None$() === x6)) {
    $f_Lcom_raquo_airstream_state_Var__set__O__V($thiz.ek, "loading the engine (8 MB, once)\u2026");
    return $m_sjs_js_Thenable$ThenableOps$().hm($i_https$003a$002f$002fcdn$002ejsdelivr$002enet$002fnpm$002f$0040duckdb$002fduckdb$002dwasm$00401$002e29$002e0$002f$002besm.selectBundle($i_https$003a$002f$002fcdn$002ejsdelivr$002enet$002fnpm$002f$0040duckdb$002fduckdb$002dwasm$00401$002e29$002e0$002f$002besm.getJsDelivrBundles())).iY(new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((bundle$2) => {
      var worker = $p_Ldpm_Main$__makeWorker__T__Lorg_scalajs_dom_Worker($thiz, bundle$2.mainWorker);
      var db = new $i_https$003a$002f$002fcdn$002ejsdelivr$002enet$002fnpm$002f$0040duckdb$002fduckdb$002dwasm$00401$002e29$002e0$002f$002besm.AsyncDuckDB(new $i_https$003a$002f$002fcdn$002ejsdelivr$002enet$002fnpm$002f$0040duckdb$002fduckdb$002dwasm$00401$002e29$002e0$002f$002besm.VoidLogger(), worker);
      return $m_sjs_js_Thenable$ThenableOps$().hm(db.instantiate(bundle$2.mainModule, bundle$2.pthreadWorker)).iY(new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((x$1$2) => $m_sjs_js_Thenable$ThenableOps$().hm(db.connect()).qz(new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((con$2) => {
        $f_Lcom_raquo_airstream_state_Var__set__O__V($thiz.i3, new $c_s_Some(con$2));
        $f_Lcom_raquo_airstream_state_Var__set__O__V($thiz.ek, "");
        return con$2;
      })), $m_s_concurrent_ExecutionContext$().g4()))), $m_s_concurrent_ExecutionContext$().g4());
    })), $m_s_concurrent_ExecutionContext$().g4());
  }
  throw new $c_s_MatchError(x6);
}
function $p_Ldpm_Main$__makeWorker__T__Lorg_scalajs_dom_Worker($thiz, url) {
  var blob = new Blob([(("importScripts(\"" + url) + "\");")], (() => {
    var this$1 = ({});
    this$1.type = "text/javascript";
    return this$1;
  })());
  return new Worker(URL.createObjectURL(blob));
}
function $p_Ldpm_Main$__ask__V($thiz) {
  var current = $f_Lcom_raquo_airstream_core_WritableSignal__tryNow__s_util_Try($thiz.gA.c3).s();
  var filled = new $c_sci_Map$WithDefault($f_Lcom_raquo_airstream_core_WritableSignal__tryNow__s_util_Try($thiz.ff.c3).s(), new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((name$2) => {
    var this$6 = current.ep;
    _return: {
      var these = this$6;
      while ((!these.c())) {
        if ((these.n().dO === name$2)) {
          var this$8 = new $c_s_Some(these.n());
          break _return;
        }
        these = these.l();
      }
      var this$8 = $m_s_None$();
    }
    var this$10 = (this$8.c() ? $m_s_None$() : new $c_s_Some(this$8.s().eq));
    return (this$10.c() ? "" : this$10.s());
  })));
  var sql = current.fi.b(filled);
  $f_Lcom_raquo_airstream_state_Var__set__O__V($thiz.fe, true);
  $f_Lcom_raquo_airstream_state_Var__set__O__V($thiz.ek, "");
  var $x_1 = $m_RTLong$().h6((+Date.now()));
  var started_$_lo = $x_1.l;
  var started_$_hi = $x_1.h;
  $p_Ldpm_Main$__connection__s_concurrent_Future($thiz).iY(new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((con$2) => $m_sjs_js_Thenable$ThenableOps$().hm(con$2.query(sql)))), $m_s_concurrent_ExecutionContext$().g4()).nX(new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((x$1$3) => {
    matchResult6: {
      if ((x$1$3 instanceof $c_s_util_Success)) {
        var table = x$1$3.cn;
        var this$20 = $ct_sjs_js_WrappedArray__sjs_js_Array__(new $c_sjs_js_WrappedArray(), table.toArray());
        $m_sci_List$();
        var this$25 = $m_sci_Nil$().eU(this$20);
        var f = ((row$2) => {
          var this$23 = $ct_sjs_js_WrappedArray__sjs_js_Array__(new $c_sjs_js_WrappedArray(), Object.entries(row$2.toJSON()));
          $m_sci_List$();
          return $m_sci_Nil$().eU(this$23);
        });
        if ((this$25 === $m_sci_Nil$())) {
          var $x_2 = $m_sci_Nil$();
        } else {
          var x0$2 = this$25.n();
          var h = new $c_sci_$colon$colon(f(x0$2), $m_sci_Nil$());
          var t = h;
          var rest = this$25.l();
          while ((rest !== $m_sci_Nil$())) {
            var x0$3 = rest.n();
            var nx = new $c_sci_$colon$colon(f(x0$3), $m_sci_Nil$());
            t.J = nx;
            t = nx;
            rest = rest.l();
          }
          var $x_2 = h;
        }
        var rows = $x_2;
        var this$26 = rows.nF();
        if (this$26.c()) {
          var this$29 = $m_s_None$();
        } else {
          var x0$4 = this$26.s();
          var f$1 = ((entry$2) => entry$2[0]);
          if ((x0$4 === $m_sci_Nil$())) {
            var $x_3 = $m_sci_Nil$();
          } else {
            var x0$5 = x0$4.n();
            var h$1 = new $c_sci_$colon$colon(f$1(x0$5), $m_sci_Nil$());
            var t$1 = h$1;
            var rest$1 = x0$4.l();
            while ((rest$1 !== $m_sci_Nil$())) {
              var x0$6 = rest$1.n();
              var nx$1 = new $c_sci_$colon$colon(f$1(x0$6), $m_sci_Nil$());
              t$1.J = nx$1;
              t$1 = nx$1;
              rest$1 = rest$1.l();
            }
            var $x_3 = h$1;
          }
          var this$29 = new $c_s_Some($x_3);
        }
        var columns = (this$29.c() ? $m_sci_Nil$() : this$29.s());
        var $x_7 = $thiz.fd;
        var f$3 = ((_$4$2) => {
          var f$2 = ((entry$2$1) => {
            var this$30 = $m_s_Option$().n9(entry$2$1[1]);
            var this$32 = (this$30.c() ? $m_s_None$() : new $c_s_Some($dp_toString__T(this$30.s())));
            return (this$32.c() ? "" : this$32.s());
          });
          if ((_$4$2 === $m_sci_Nil$())) {
            var $x_4 = $m_sci_Nil$();
          } else {
            var x0$8 = _$4$2.n();
            var h$2 = new $c_sci_$colon$colon(f$2(x0$8), $m_sci_Nil$());
            var t$2 = h$2;
            var rest$2 = _$4$2.l();
            while ((rest$2 !== $m_sci_Nil$())) {
              var x0$9 = rest$2.n();
              var nx$2 = new $c_sci_$colon$colon(f$2(x0$9), $m_sci_Nil$());
              t$2.J = nx$2;
              t$2 = nx$2;
              rest$2 = rest$2.l();
            }
            var $x_4 = h$2;
          }
          return $x_4;
        });
        if ((rows === $m_sci_Nil$())) {
          var $x_5 = $m_sci_Nil$();
        } else {
          var x0$10 = rows.n();
          var h$3 = new $c_sci_$colon$colon(f$3(x0$10), $m_sci_Nil$());
          var t$3 = h$3;
          var rest$3 = rows.l();
          while ((rest$3 !== $m_sci_Nil$())) {
            var x0$11 = rest$3.n();
            var nx$3 = new $c_sci_$colon$colon(f$3(x0$11), $m_sci_Nil$());
            t$3.J = nx$3;
            t$3 = nx$3;
            rest$3 = rest$3.l();
          }
          var $x_5 = h$3;
        }
        var rows$1 = $x_5;
        var $x_6 = $m_RTLong$().h6((+Date.now()));
        var x_$_lo = $x_6.l;
        var x_$_hi = $x_6.h;
        var lo = ((x_$_lo - started_$_lo) | 0);
        var hi = ((((x_$_hi - started_$_hi) | 0) - (((lo >>> 0) > (x_$_lo >>> 0)) | 0)) | 0);
        var source = current.rg(filled);
        $f_Lcom_raquo_airstream_state_Var__set__O__V($x_7, new $c_s_Some(new $c_Ldpm_Main$Answer(columns, rows$1, lo, hi, sql, source)));
        $f_Lcom_raquo_airstream_state_Var__set__O__V($thiz.fe, false);
        break matchResult6;
      }
      if ((x$1$3 instanceof $c_s_util_Failure)) {
        var problem = x$1$3.c7;
        $f_Lcom_raquo_airstream_state_Var__set__O__V($thiz.ek, problem.eS());
        $f_Lcom_raquo_airstream_state_Var__set__O__V($thiz.fd, $m_s_None$());
        $f_Lcom_raquo_airstream_state_Var__set__O__V($thiz.fe, false);
        break matchResult6;
      }
      throw new $c_s_MatchError(x$1$3);
    }
  })), $m_s_concurrent_ExecutionContext$().g4());
}
function $p_Ldpm_Main$__page__Lcom_raquo_laminar_nodes_ReactiveHtmlElement($thiz) {
  var $x_12 = $m_Lcom_raquo_laminar_api_package$().o.iS();
  var $x_11 = $m_Lcom_raquo_laminar_api_package$().o.dL.eJ("page");
  var $x_10 = $m_Lcom_raquo_laminar_api_package$().o.qg().ad(new $c_sjsr_WrappedVarArgs([$f_Lcom_raquo_laminar_api_Implicits__textToTextNode__O__Lcom_raquo_laminar_modifiers_RenderableText__Lcom_raquo_laminar_nodes_TextNode($m_Lcom_raquo_laminar_api_package$().o, "The EBA data point model, in your browser", $m_Lcom_raquo_laminar_modifiers_RenderableText$().br)]));
  var $x_9 = $m_Lcom_raquo_laminar_api_package$().o.jn().ad(new $c_sjsr_WrappedVarArgs([$m_Lcom_raquo_laminar_api_package$().o.dL.eJ("lede"), $f_Lcom_raquo_laminar_api_Implicits__textToTextNode__O__Lcom_raquo_laminar_modifiers_RenderableText__Lcom_raquo_laminar_nodes_TextNode($m_Lcom_raquo_laminar_api_package$().o, "Pick a question and fill it in. Every answer shows the SQL that produced it, and the ", $m_Lcom_raquo_laminar_modifiers_RenderableText$().br), $f_Lcom_raquo_laminar_api_Implicits__textToTextNode__O__Lcom_raquo_laminar_modifiers_RenderableText__Lcom_raquo_laminar_nodes_TextNode($m_Lcom_raquo_laminar_api_package$().o, "file it read. No server: DuckDB-WASM queries parquet over HTTP range requests.", $m_Lcom_raquo_laminar_modifiers_RenderableText$().br)]));
  var $x_8 = $m_Lcom_raquo_laminar_api_package$().o.iS();
  var $x_7 = $m_Lcom_raquo_laminar_api_package$().o.dL.eJ("controls");
  var $x_6 = $m_Lcom_raquo_laminar_api_package$().o.nN();
  var $x_5 = $f_Lcom_raquo_laminar_api_Implicits__textToTextNode__O__Lcom_raquo_laminar_modifiers_RenderableText__Lcom_raquo_laminar_nodes_TextNode($m_Lcom_raquo_laminar_api_package$().o, "Question", $m_Lcom_raquo_laminar_modifiers_RenderableText$().br);
  var $x_4 = $m_Lcom_raquo_laminar_api_package$().o.r9();
  var $x_3 = new $c_Lcom_raquo_laminar_modifiers_EventListener(($m_Lcom_raquo_laminar_api_package$(), $m_Lcom_raquo_laminar_keys_EventProcessor$().h4($m_Lcom_raquo_laminar_api_package$().o.nV(), false, false)).nP(), new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((id$3) => {
    $f_Lcom_raquo_airstream_state_Var__set__O__V($thiz.gA, $m_Ldpm_Questions$().pp(id$3));
    $f_Lcom_raquo_airstream_state_Var__set__O__V($thiz.ff, $m_sci_Map$EmptyMap$());
    $f_Lcom_raquo_airstream_state_Var__set__O__V($thiz.fd, $m_s_None$());
  })));
  var $x_2 = $m_Lcom_raquo_laminar_api_package$().o;
  var this$23 = $m_Ldpm_Questions$().fj;
  var f = ((q$2) => $m_Lcom_raquo_laminar_api_package$().o.qL().ad(new $c_sjsr_WrappedVarArgs([$m_Lcom_raquo_laminar_api_package$().o.hn().mV(q$2.eo), $f_Lcom_raquo_laminar_api_Implicits__textToTextNode__O__Lcom_raquo_laminar_modifiers_RenderableText__Lcom_raquo_laminar_nodes_TextNode($m_Lcom_raquo_laminar_api_package$().o, q$2.fg, $m_Lcom_raquo_laminar_modifiers_RenderableText$().br)])));
  if ((this$23 === $m_sci_Nil$())) {
    var $x_1 = $m_sci_Nil$();
  } else {
    var x0$3 = this$23.n();
    var h = new $c_sci_$colon$colon(f(x0$3), $m_sci_Nil$());
    var t = h;
    var rest = this$23.l();
    while ((rest !== $m_sci_Nil$())) {
      var x0$4 = rest.n();
      var nx = new $c_sci_$colon$colon(f(x0$4), $m_sci_Nil$());
      t.J = nx;
      t = nx;
      rest = rest.l();
    }
    var $x_1 = h;
  }
  return $x_12.ad(new $c_sjsr_WrappedVarArgs([$x_11, $x_10, $x_9, $x_8.ad(new $c_sjsr_WrappedVarArgs([$x_7, $x_6.ad(new $c_sjsr_WrappedVarArgs([$x_5, $x_4.ad(new $c_sjsr_WrappedVarArgs([$x_3, $f_Lcom_raquo_laminar_api_Implicits__nodeSeqToModifier__O__Lcom_raquo_laminar_modifiers_RenderableSeq__Lcom_raquo_laminar_modifiers_Modifier($x_2, $x_1, $m_Lcom_raquo_laminar_modifiers_RenderableSeq$collectionSeqRenderable$())]))])), ($m_Lcom_raquo_laminar_api_package$(), $m_Lcom_raquo_laminar_inserters_ChildrenInserter$().p9(new $c_Lcom_raquo_airstream_misc_MapSignal($thiz.gA.c3, new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((current$2) => {
    var this$47 = current$2.ep;
    var f$1 = ((slot$2) => $m_Lcom_raquo_laminar_api_package$().o.nN().ad(new $c_sjsr_WrappedVarArgs([$f_Lcom_raquo_laminar_api_Implicits__textToTextNode__O__Lcom_raquo_laminar_modifiers_RenderableText__Lcom_raquo_laminar_nodes_TextNode($m_Lcom_raquo_laminar_api_package$().o, slot$2.fk, $m_Lcom_raquo_laminar_modifiers_RenderableText$().br), $m_Lcom_raquo_laminar_api_package$().o.qn().ad(new $c_sjsr_WrappedVarArgs([$m_Lcom_raquo_laminar_api_package$().o.qN().mV(slot$2.fl), $m_Lcom_raquo_laminar_api_package$().o.hn().mW(new $c_Lcom_raquo_airstream_misc_MapSignal($thiz.ff.c3, new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((slot$1) => ((_$6$2) => _$6$2.c9(slot$1.dO, new $c_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c((() => slot$1.eq)))))(slot$2)), $m_s_None$())), new $c_Lcom_raquo_laminar_modifiers_EventListener(($m_Lcom_raquo_laminar_api_package$(), $m_Lcom_raquo_laminar_keys_EventProcessor$().h4($m_Lcom_raquo_laminar_api_package$().o.he(), false, false)).nP(), new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((slot$5) => ((text$3) => {
      $f_Lcom_raquo_airstream_state_Var__update__F1__V($thiz.ff, new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((text$1) => ((_$7$2) => _$7$2.cd(slot$5.dO, text$1)))(text$3)));
    }))(slot$2)))]))])));
    if ((this$47 === $m_sci_Nil$())) {
      var $x_13 = $m_sci_Nil$();
    } else {
      var x0$9 = this$47.n();
      var h$1 = new $c_sci_$colon$colon(f$1(x0$9), $m_sci_Nil$());
      var t$1 = h$1;
      var rest$1 = this$47.l();
      while ((rest$1 !== $m_sci_Nil$())) {
        var x0$10 = rest$1.n();
        var nx$1 = new $c_sci_$colon$colon(f$1(x0$10), $m_sci_Nil$());
        t$1.J = nx$1;
        t$1 = nx$1;
        rest$1 = rest$1.l();
      }
      var $x_13 = h$1;
    }
    return $x_13;
  })), $m_s_None$()), $m_Lcom_raquo_laminar_modifiers_RenderableSeq$collectionSeqRenderable$(), $m_Lcom_raquo_laminar_modifiers_RenderableNode$().hU, (void 0))), $m_Lcom_raquo_laminar_api_package$().o.po().ad(new $c_sjsr_WrappedVarArgs([$f_Lcom_raquo_laminar_api_Implicits__textToTextNode__O__Lcom_raquo_laminar_modifiers_RenderableText__Lcom_raquo_laminar_nodes_TextNode($m_Lcom_raquo_laminar_api_package$().o, "Ask", $m_Lcom_raquo_laminar_modifiers_RenderableText$().br), $m_Lcom_raquo_laminar_api_package$().o.pK().mW($thiz.fe.c3), new $c_Lcom_raquo_laminar_modifiers_EventListener(($m_Lcom_raquo_laminar_api_package$(), $m_Lcom_raquo_laminar_keys_EventProcessor$().h4($m_Lcom_raquo_laminar_api_package$().o.nW(), false, false)), new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((_$8$3) => {
    $p_Ldpm_Main$__ask__V($thiz);
  })))]))])), $m_Lcom_raquo_laminar_api_package$().o.jn().ad(new $c_sjsr_WrappedVarArgs([$m_Lcom_raquo_laminar_api_package$().o.dL.eJ("status"), ($m_Lcom_raquo_laminar_api_package$(), $m_Lcom_raquo_laminar_inserters_ChildTextInserter$().pa($thiz.ek.c3, $m_Lcom_raquo_laminar_modifiers_RenderableText$().br))])), ($m_Lcom_raquo_laminar_api_package$(), $m_Lcom_raquo_laminar_inserters_ChildInserter$().p8(new $c_Lcom_raquo_airstream_misc_MapSignal($thiz.fd.c3, new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((x$1$2) => {
    if (($m_s_None$() === x$1$2)) {
      $m_Lcom_raquo_laminar_api_package$();
      return new $c_Lcom_raquo_laminar_nodes_CommentNode("");
    }
    if ((x$1$2 instanceof $c_s_Some)) {
      var result = x$1$2.cC;
      var $x_28 = $m_Lcom_raquo_laminar_api_package$().o.iS();
      var $x_27 = $m_Lcom_raquo_laminar_api_package$().o.dL.eJ("answer");
      var $x_26 = $m_Lcom_raquo_laminar_api_package$().o.jn().ad(new $c_sjsr_WrappedVarArgs([$m_Lcom_raquo_laminar_api_package$().o.dL.eJ("meta"), $f_Lcom_raquo_laminar_api_Implicits__textToTextNode__O__Lcom_raquo_laminar_modifiers_RenderableText__Lcom_raquo_laminar_nodes_TextNode($m_Lcom_raquo_laminar_api_package$().o, ((((result.dN.q() + " row(s) in ") + $s_RTLong__toString__I__I__T(result.eH, result.eI)) + " ms, read from ") + result.em), $m_Lcom_raquo_laminar_modifiers_RenderableText$().br)]));
      var $x_25 = $m_Lcom_raquo_laminar_api_package$().o.rr();
      var $x_24 = $m_Lcom_raquo_laminar_api_package$().o.ry();
      var $x_23 = $m_Lcom_raquo_laminar_api_package$().o.oj();
      var $x_22 = $m_Lcom_raquo_laminar_api_package$().o;
      var this$75 = result.el;
      var f$2 = ((_$9$2) => $m_Lcom_raquo_laminar_api_package$().o.rx().ad(new $c_sjsr_WrappedVarArgs([$f_Lcom_raquo_laminar_api_Implicits__textToTextNode__O__Lcom_raquo_laminar_modifiers_RenderableText__Lcom_raquo_laminar_nodes_TextNode($m_Lcom_raquo_laminar_api_package$().o, _$9$2, $m_Lcom_raquo_laminar_modifiers_RenderableText$().br)])));
      if ((this$75 === $m_sci_Nil$())) {
        var $x_21 = $m_sci_Nil$();
      } else {
        var x0$16 = this$75.n();
        var h$2 = new $c_sci_$colon$colon(f$2(x0$16), $m_sci_Nil$());
        var t$2 = h$2;
        var rest$2 = this$75.l();
        while ((rest$2 !== $m_sci_Nil$())) {
          var x0$17 = rest$2.n();
          var nx$2 = new $c_sci_$colon$colon(f$2(x0$17), $m_sci_Nil$());
          t$2.J = nx$2;
          t$2 = nx$2;
          rest$2 = rest$2.l();
        }
        var $x_21 = h$2;
      }
      var $x_20 = $x_24.ad(new $c_sjsr_WrappedVarArgs([$x_23.ad(new $c_sjsr_WrappedVarArgs([$f_Lcom_raquo_laminar_api_Implicits__nodeSeqToModifier__O__Lcom_raquo_laminar_modifiers_RenderableSeq__Lcom_raquo_laminar_modifiers_Modifier($x_22, $x_21, $m_Lcom_raquo_laminar_modifiers_RenderableSeq$collectionSeqRenderable$())]))]));
      var $x_19 = $m_Lcom_raquo_laminar_api_package$().o.ru();
      var $x_18 = $m_Lcom_raquo_laminar_api_package$().o;
      var this$91 = result.dN.rt(200);
      var f$4 = ((row$2) => {
        var $x_16 = $m_Lcom_raquo_laminar_api_package$().o.oj();
        var $x_15 = $m_Lcom_raquo_laminar_api_package$().o;
        var f$3 = ((_$10$2) => $m_Lcom_raquo_laminar_api_package$().o.rv().ad(new $c_sjsr_WrappedVarArgs([$f_Lcom_raquo_laminar_api_Implicits__textToTextNode__O__Lcom_raquo_laminar_modifiers_RenderableText__Lcom_raquo_laminar_nodes_TextNode($m_Lcom_raquo_laminar_api_package$().o, _$10$2, $m_Lcom_raquo_laminar_modifiers_RenderableText$().br)])));
        if ((row$2 === $m_sci_Nil$())) {
          var $x_14 = $m_sci_Nil$();
        } else {
          var x0$21 = row$2.n();
          var h$3 = new $c_sci_$colon$colon(f$3(x0$21), $m_sci_Nil$());
          var t$3 = h$3;
          var rest$3 = row$2.l();
          while ((rest$3 !== $m_sci_Nil$())) {
            var x0$22 = rest$3.n();
            var nx$3 = new $c_sci_$colon$colon(f$3(x0$22), $m_sci_Nil$());
            t$3.J = nx$3;
            t$3 = nx$3;
            rest$3 = rest$3.l();
          }
          var $x_14 = h$3;
        }
        return $x_16.ad(new $c_sjsr_WrappedVarArgs([$f_Lcom_raquo_laminar_api_Implicits__nodeSeqToModifier__O__Lcom_raquo_laminar_modifiers_RenderableSeq__Lcom_raquo_laminar_modifiers_Modifier($x_15, $x_14, $m_Lcom_raquo_laminar_modifiers_RenderableSeq$collectionSeqRenderable$())]));
      });
      if ((this$91 === $m_sci_Nil$())) {
        var $x_17 = $m_sci_Nil$();
      } else {
        var x0$24 = this$91.n();
        var h$4 = new $c_sci_$colon$colon(f$4(x0$24), $m_sci_Nil$());
        var t$4 = h$4;
        var rest$4 = this$91.l();
        while ((rest$4 !== $m_sci_Nil$())) {
          var x0$25 = rest$4.n();
          var nx$4 = new $c_sci_$colon$colon(f$4(x0$25), $m_sci_Nil$());
          t$4.J = nx$4;
          t$4 = nx$4;
          rest$4 = rest$4.l();
        }
        var $x_17 = h$4;
      }
      return $x_28.ad(new $c_sjsr_WrappedVarArgs([$x_27, $x_26, $x_25.ad(new $c_sjsr_WrappedVarArgs([$x_20, $x_19.ad(new $c_sjsr_WrappedVarArgs([$f_Lcom_raquo_laminar_api_Implicits__nodeSeqToModifier__O__Lcom_raquo_laminar_modifiers_RenderableSeq__Lcom_raquo_laminar_modifiers_Modifier($x_18, $x_17, $m_Lcom_raquo_laminar_modifiers_RenderableSeq$collectionSeqRenderable$())]))])), $m_Lcom_raquo_laminar_api_package$().o.pI().ad(new $c_sjsr_WrappedVarArgs([$m_Lcom_raquo_laminar_api_package$().o.rl().ad(new $c_sjsr_WrappedVarArgs([$f_Lcom_raquo_laminar_api_Implicits__textToTextNode__O__Lcom_raquo_laminar_modifiers_RenderableText__Lcom_raquo_laminar_nodes_TextNode($m_Lcom_raquo_laminar_api_package$().o, "the SQL that answered it", $m_Lcom_raquo_laminar_modifiers_RenderableText$().br)])), $m_Lcom_raquo_laminar_api_package$().o.qO().ad(new $c_sjsr_WrappedVarArgs([$m_Lcom_raquo_laminar_api_package$().o.pt().ad(new $c_sjsr_WrappedVarArgs([$f_Lcom_raquo_laminar_api_Implicits__textToTextNode__O__Lcom_raquo_laminar_modifiers_RenderableText__Lcom_raquo_laminar_nodes_TextNode($m_Lcom_raquo_laminar_api_package$().o, result.en, $m_Lcom_raquo_laminar_modifiers_RenderableText$().br)]))]))]))]));
    }
    throw new $c_s_MatchError(x$1$2);
  })), $m_s_None$()), $m_Lcom_raquo_laminar_modifiers_RenderableNode$().hU, (void 0)))]));
}
/** @constructor */
function $c_Ldpm_Main$() {
  this.i3 = null;
  this.ek = null;
  this.fe = null;
  this.fd = null;
  this.gA = null;
  this.ff = null;
  $n_Ldpm_Main$ = this;
  this.i3 = $m_Lcom_raquo_laminar_api_package$().o.dK.eN($m_s_None$());
  this.ek = $m_Lcom_raquo_laminar_api_package$().o.dK.eN("");
  this.fe = $m_Lcom_raquo_laminar_api_package$().o.dK.eN(false);
  this.fd = $m_Lcom_raquo_laminar_api_package$().o.dK.eN($m_s_None$());
  this.gA = $m_Lcom_raquo_laminar_api_package$().o.dK.eN($m_Ldpm_Questions$().fj.n());
  this.ff = $m_Lcom_raquo_laminar_api_package$().o.dK.eN($m_sci_Map$EmptyMap$());
}
$p = $c_Ldpm_Main$.prototype = new $h_O();
$p.constructor = $c_Ldpm_Main$;
/** @constructor */
function $h_Ldpm_Main$() {
}
$h_Ldpm_Main$.prototype = $p;
$p.qy = (function(args) {
  var this$3 = $m_Lcom_raquo_laminar_api_package$().o;
  var container = new $c_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c((() => document.getElementById("app")));
  var rootNode = new $c_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c((() => $p_Ldpm_Main$__page__Lcom_raquo_laminar_nodes_ReactiveHtmlElement(this)));
  var p = $m_Lcom_raquo_laminar_keys_EventProcessor$().h4(this$3.kK.qK(), false, false);
  $f_Lcom_raquo_airstream_core_BaseObservable__foreach__F1__Lcom_raquo_airstream_ownership_Owner__Lcom_raquo_airstream_ownership_Subscription(new $c_Lcom_raquo_airstream_misc_CollectStream($m_Lcom_raquo_airstream_web_DomEventStream$().pd(document, p.ei.f9, p.gw), p.gv), new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((_$2) => {
    new $c_Lcom_raquo_laminar_nodes_RootNode(container.F(), rootNode.F());
  })), this$3.rG());
});
var $d_Ldpm_Main$ = new $TypeData().i($c_Ldpm_Main$, "dpm.Main$", ({
  er: 1
}));
var $n_Ldpm_Main$;
function $m_Ldpm_Main$() {
  if ((!$n_Ldpm_Main$)) {
    $n_Ldpm_Main$ = new $c_Ldpm_Main$();
  }
  return $n_Ldpm_Main$;
}
function $p_Ldpm_Questions$__partition__T__T__T($thiz, table, framework) {
  return $m_Ldpm_Data$().oo((((table + "/framework=") + framework) + "/data_0.parquet"));
}
function $p_Ldpm_Questions$__whole__T__T__T($thiz, table, framework) {
  return $m_Ldpm_Data$().oo((table + ".parquet"));
}
/** @constructor */
function $c_Ldpm_Questions$() {
  this.fj = null;
  $n_Ldpm_Questions$ = this;
  var framework = new $c_Ldpm_Slot("framework", "Framework", "FINREP, COREP, DORA\u2026", "FINREP");
  var template = new $c_Ldpm_Slot("table", "Template", "F_12.01.a", "F_12.01.a");
  $m_sci_List$();
  var elems = new $c_sjsr_WrappedVarArgs([framework, template, new $c_Ldpm_Slot("module", "Module", "FINREP9", "FINREP9")]);
  this.fj = new $c_sci_$colon$colon(new $c_Ldpm_Question("cells", "Which cells does a template have?", $m_sci_Nil$().eU(elems), new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((filled$2) => $f_T__trim__T($m_sc_StringOps$().gh((((((("\n        |SELECT row_code, row_label, column_code, column_label, datapoint, cell_code\n        |FROM   '" + $p_Ldpm_Questions$__partition__T__T__T(this, "cells", filled$2.b("framework"))) + "'\n        |WHERE  table_code = '") + filled$2.b("table")) + "' AND module = '") + filled$2.b("module")) + "'\n        |ORDER  BY row_code, column_code\n        |LIMIT  200"), 124)))), new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((framework$2) => $p_Ldpm_Questions$__partition__T__T__T(this, "cells", framework$2)))), new $c_sci_$colon$colon(new $c_Ldpm_Question("dimensions", "What does a template break down by?", new $c_sci_$colon$colon(framework, new $c_sci_$colon$colon(template, $m_sci_Nil$())), new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((filled$2$1) => $f_T__trim__T($m_sc_StringOps$().gh((((("\n        |SELECT   dimension, count(DISTINCT member) AS members,\n        |         string_agg(DISTINCT member, ', ' ORDER BY member) AS wording\n        |FROM     '" + $p_Ldpm_Questions$__partition__T__T__T(this, "cell_members", filled$2$1.b("framework"))) + "'\n        |WHERE    table_code = '") + filled$2$1.b("table")) + "'\n        |GROUP BY dimension\n        |ORDER BY dimension"), 124)))), new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((framework$2$1) => $p_Ldpm_Questions$__partition__T__T__T(this, "cell_members", framework$2$1)))), new $c_sci_$colon$colon(new $c_Ldpm_Question("rule", "What does a validation code mean?", new $c_sci_$colon$colon(new $c_Ldpm_Slot("rule_code", "Rule code", "v0174_m", "v0174_m"), $m_sci_Nil$()), new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((filled$2$2) => $f_T__trim__T($m_sc_StringOps$().gh((((("\n        |SELECT module, taxonomy_version, dpm_release, severity, active,\n        |       from_submission_date, expression\n        |FROM   '" + $p_Ldpm_Questions$__whole__T__T__T(this, "rules", "")) + "'\n        |WHERE  rule_code = regexp_replace('") + filled$2$2.b("rule_code")) + "', '_[0-9]+$', '')\n        |ORDER  BY module, taxonomy_version"), 124)))), new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((framework$2$2) => $p_Ldpm_Questions$__whole__T__T__T(this, "rules", framework$2$2)))), new $c_sci_$colon$colon(new $c_Ldpm_Question("keys", "What are a template's key dimensions?", new $c_sci_$colon$colon(framework, new $c_sci_$colon$colon(template, $m_sci_Nil$())), new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((filled$2$3) => $f_T__trim__T($m_sc_StringOps$().gh((((("\n        |SELECT code, label, property_code, property\n        |FROM   '" + $p_Ldpm_Questions$__whole__T__T__T(this, "headers", "")) + "'\n        |WHERE  table_code = '") + filled$2$3.b("table")) + "' AND is_key\n        |ORDER  BY code"), 124)))), new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((framework$2$3) => $p_Ldpm_Questions$__whole__T__T__T(this, "headers", framework$2$3)))), new $c_sci_$colon$colon(new $c_Ldpm_Question("modules", "Which module versions is a framework reported under?", new $c_sci_$colon$colon(framework, $m_sci_Nil$()), new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((filled$2$4) => $f_T__trim__T($m_sc_StringOps$().gh((((("\n        |SELECT module, taxonomy_version, dpm_release, from_reference_date,\n        |       to_reference_date, do_not_use\n        |FROM   '" + $p_Ldpm_Questions$__whole__T__T__T(this, "modules", "")) + "'\n        |WHERE  framework = '") + filled$2$4.b("framework")) + "'\n        |ORDER  BY module, taxonomy_version"), 124)))), new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((framework$2$4) => $p_Ldpm_Questions$__whole__T__T__T(this, "modules", framework$2$4)))), $m_sci_Nil$())))));
}
$p = $c_Ldpm_Questions$.prototype = new $h_O();
$p.constructor = $c_Ldpm_Questions$;
/** @constructor */
function $h_Ldpm_Questions$() {
}
$h_Ldpm_Questions$.prototype = $p;
$p.pp = (function(id) {
  var this$1 = this.fj;
  _return: {
    var these = this$1;
    while ((!these.c())) {
      if ((these.n().eo === id)) {
        var this$3 = new $c_s_Some(these.n());
        break _return;
      }
      these = these.l();
    }
    var this$3 = $m_s_None$();
  }
  return (this$3.c() ? this.fj.n() : this$3.s());
});
var $d_Ldpm_Questions$ = new $TypeData().i($c_Ldpm_Questions$, "dpm.Questions$", ({
  es: 1
}));
var $n_Ldpm_Questions$;
function $m_Ldpm_Questions$() {
  if ((!$n_Ldpm_Questions$)) {
    $n_Ldpm_Questions$ = new $c_Ldpm_Questions$();
  }
  return $n_Ldpm_Questions$;
}
var $d_jl_Runnable = new $TypeData().i(1, "java.lang.Runnable", ({
  aE: 1
}));
function $p_jl_StackTrace$__normalizedLinesToStackTrace__O__Ajl_StackTraceElement($thiz, lines) {
  var NormalizedFrameLine = $m_jl_StackTrace$StringRE$().cb("^([^@]*)@(.*?):([0-9]+)(?::([0-9]+))?$");
  var trace = [];
  var i = 0;
  while ((i < (lines.length | 0))) {
    var line = lines[i];
    if ((line !== "")) {
      var mtch = NormalizedFrameLine.exec(line);
      if ((mtch !== null)) {
        var classAndMethodName = $p_jl_StackTrace$__extractClassMethod__T__O($thiz, mtch[1]);
        var $x_5 = classAndMethodName[0];
        var $x_4 = classAndMethodName[1];
        var $x_3 = mtch[2];
        var x$2 = mtch[3];
        var $x_2 = parseInt(x$2);
        var x$3 = mtch[4];
        var $x_1 = trace.push(new $c_jl_StackTraceElement($x_5, $x_4, $x_3, ($x_2 | 0), ((x$3 !== (void 0)) ? (parseInt(x$3) | 0) : (-1))));
      } else {
        (trace.push(new $c_jl_StackTraceElement("<jscode>", line, null, (-1), (-1))) | 0);
      }
    }
    i = ((1 + i) | 0);
  }
  var len = (trace.length | 0);
  var result = new ($d_jl_StackTraceElement.r().C)(len);
  i = 0;
  while ((i < len)) {
    result.a[i] = trace[i];
    i = ((1 + i) | 0);
  }
  return result;
}
function $p_jl_StackTrace$__extractClassMethod__T__O($thiz, functionName) {
  var PatBC = $m_jl_StackTrace$StringRE$().cb("^(?:Object\\.|\\[object Object\\]\\.|Module\\.)?\\$[bc]_([^\\.]+)(?:\\.prototype)?\\.([^\\.]+)$");
  var PatS = $m_jl_StackTrace$StringRE$().cb("^(?:Object\\.|\\[object Object\\]\\.|Module\\.)?\\$(?:ps?|s|f)_((?:_[^_]|[^_])+)__([^\\.]+)$");
  var PatCT = $m_jl_StackTrace$StringRE$().cb("^(?:Object\\.|\\[object Object\\]\\.|Module\\.)?\\$ct_((?:_[^_]|[^_])+)__([^\\.]*)$");
  var PatN = $m_jl_StackTrace$StringRE$().cb("^new (?:Object\\.|\\[object Object\\]\\.|Module\\.)?\\$c_([^\\.]+)$");
  var PatM = $m_jl_StackTrace$StringRE$().cb("^(?:Object\\.|\\[object Object\\]\\.|Module\\.)?\\$m_([^\\.]+)$");
  var matchBC = PatBC.exec(functionName);
  var matchBCOrS = ((matchBC !== null) ? matchBC : PatS.exec(functionName));
  if ((matchBCOrS !== null)) {
    return [$p_jl_StackTrace$__decodeClassName__T__T($thiz, matchBCOrS[1]), $p_jl_StackTrace$__decodeMethodName__T__T($thiz, matchBCOrS[2])];
  } else {
    var matchCT = PatCT.exec(functionName);
    var matchCTOrN = ((matchCT !== null) ? matchCT : PatN.exec(functionName));
    if ((matchCTOrN !== null)) {
      return [$p_jl_StackTrace$__decodeClassName__T__T($thiz, matchCTOrN[1]), "<init>"];
    } else {
      var matchM = PatM.exec(functionName);
      return ((matchM !== null) ? [$p_jl_StackTrace$__decodeClassName__T__T($thiz, matchM[1]), "<clinit>"] : ["<jscode>", functionName]);
    }
  }
}
function $p_jl_StackTrace$__decodeClassName__T__T($thiz, encodedName) {
  var dict = $p_jl_StackTrace$__decompressedClasses__O($thiz);
  if ((!(!$m_jl_Utils$Cache$().ib.call(dict, encodedName)))) {
    var dict$1 = $p_jl_StackTrace$__decompressedClasses__O($thiz);
    var base = dict$1[encodedName];
  } else {
    var base = $p_jl_StackTrace$__loop$1__I__T__T($thiz, 0, encodedName);
  }
  var this$3 = base.split("_").join(".");
  return this$3.split("\uff3f").join("_");
}
function $p_jl_StackTrace$__decompressedClasses$lzycompute__O($thiz) {
  if (((((1 & $thiz.bK) << 24) >> 24) === 0)) {
    var dict = ({});
    dict.O = "java_lang_Object";
    dict.T = "java_lang_String";
    var index = 0;
    while ((index <= 22)) {
      if ((index >= 2)) {
        var key = ("T" + index);
        var value = ("scala_Tuple" + index);
        dict[key] = value;
      }
      var key$1 = ("F" + index);
      var value$1 = ("scala_Function" + index);
      dict[key$1] = value$1;
      index = ((1 + index) | 0);
    }
    $thiz.i7 = dict;
    $thiz.bK = (((1 | $thiz.bK) << 24) >> 24);
  }
  return $thiz.i7;
}
function $p_jl_StackTrace$__decompressedClasses__O($thiz) {
  return (((((1 & $thiz.bK) << 24) >> 24) === 0) ? $p_jl_StackTrace$__decompressedClasses$lzycompute__O($thiz) : $thiz.i7);
}
function $p_jl_StackTrace$__decompressedPrefixes$lzycompute__O($thiz) {
  if (((((2 & $thiz.bK) << 24) >> 24) === 0)) {
    var dict = ({});
    dict.sjsr_ = "scala_scalajs_runtime_";
    dict.sjs_ = "scala_scalajs_";
    dict.sci_ = "scala_collection_immutable_";
    dict.scm_ = "scala_collection_mutable_";
    dict.scg_ = "scala_collection_generic_";
    dict.sc_ = "scala_collection_";
    dict.sr_ = "scala_runtime_";
    dict.s_ = "scala_";
    dict.jl_ = "java_lang_";
    dict.ju_ = "java_util_";
    $thiz.i8 = dict;
    $thiz.bK = (((2 | $thiz.bK) << 24) >> 24);
  }
  return $thiz.i8;
}
function $p_jl_StackTrace$__decompressedPrefixes__O($thiz) {
  return (((((2 & $thiz.bK) << 24) >> 24) === 0) ? $p_jl_StackTrace$__decompressedPrefixes$lzycompute__O($thiz) : $thiz.i8);
}
function $p_jl_StackTrace$__compressedPrefixes$lzycompute__O($thiz) {
  if (((((4 & $thiz.bK) << 24) >> 24) === 0)) {
    $thiz.i6 = Object.keys($p_jl_StackTrace$__decompressedPrefixes__O($thiz));
    $thiz.bK = (((4 | $thiz.bK) << 24) >> 24);
  }
  return $thiz.i6;
}
function $p_jl_StackTrace$__compressedPrefixes__O($thiz) {
  return (((((4 & $thiz.bK) << 24) >> 24) === 0) ? $p_jl_StackTrace$__compressedPrefixes$lzycompute__O($thiz) : $thiz.i6);
}
function $p_jl_StackTrace$__decodeMethodName__T__T($thiz, encodedName) {
  if ((!(!encodedName.startsWith("init___")))) {
    return "<init>";
  } else {
    var methodNameLen = (encodedName.indexOf("__") | 0);
    return ((methodNameLen < 0) ? encodedName : encodedName.substring(0, methodNameLen));
  }
}
function $p_jl_StackTrace$__normalizeStackTraceLines__O__O($thiz, e) {
  return ((!(!(!(!(!e))))) ? [] : ((!(!(!(!(e.arguments && e.stack))))) ? $p_jl_StackTrace$__extractChrome__O__O($thiz, e) : ((!(!(!(!(e.stack && e.sourceURL))))) ? $p_jl_StackTrace$__extractSafari__O__O($thiz, e) : ((!(!(!(!(e.stack && e.number))))) ? $p_jl_StackTrace$__extractIE__O__O($thiz, e) : ((!(!(!(!(e.stack && e.fileName))))) ? $p_jl_StackTrace$__extractFirefox__O__O($thiz, e) : ((!(!(!(!(e.message && e["opera#sourceloc"]))))) ? ((!(!(!(!(!e.stacktrace))))) ? $p_jl_StackTrace$__extractOpera9__O__O($thiz, e) : ((!(!(!(!((e.message.indexOf("\n") > (-1.0)) && (e.message.split("\n").length > e.stacktrace.split("\n").length)))))) ? $p_jl_StackTrace$__extractOpera9__O__O($thiz, e) : $p_jl_StackTrace$__extractOpera10a__O__O($thiz, e))) : ((!(!(!(!((e.message && e.stack) && e.stacktrace))))) ? ((!(!(!(!(e.stacktrace.indexOf("called from line") < 0.0))))) ? $p_jl_StackTrace$__extractOpera10b__O__O($thiz, e) : $p_jl_StackTrace$__extractOpera11__O__O($thiz, e)) : ((!(!(!(!(e.stack && (!e.fileName)))))) ? $p_jl_StackTrace$__extractChrome__O__O($thiz, e) : $p_jl_StackTrace$__extractOther__O__O($thiz, e)))))))));
}
function $p_jl_StackTrace$__extractChrome__O__O($thiz, e) {
  return (e.stack + "\n").replace($m_jl_StackTrace$StringRE$().cb("^[\\s\\S]+?\\s+at\\s+"), " at ").replace($m_jl_StackTrace$StringRE$().by("^\\s+(at eval )?at\\s+", "gm"), "").replace($m_jl_StackTrace$StringRE$().by("^([^\\(]+?)([\\n])", "gm"), "{anonymous}() ($1)$2").replace($m_jl_StackTrace$StringRE$().by("^Object.<anonymous>\\s*\\(([^\\)]+)\\)", "gm"), "{anonymous}() ($1)").replace($m_jl_StackTrace$StringRE$().by("^([^\\(]+|\\{anonymous\\}\\(\\)) \\((.+)\\)$", "gm"), "$1@$2").split("\n").slice(0, (-1));
}
function $p_jl_StackTrace$__extractFirefox__O__O($thiz, e) {
  return e.stack.replace($m_jl_StackTrace$StringRE$().by("(?:\\n@:0)?\\s+$", "m"), "").replace($m_jl_StackTrace$StringRE$().by("^(?:\\((\\S*)\\))?@", "gm"), "{anonymous}($1)@").split("\n");
}
function $p_jl_StackTrace$__extractIE__O__O($thiz, e) {
  var qual$1 = e.stack.replace($m_jl_StackTrace$StringRE$().by("^\\s*at\\s+(.*)$", "gm"), "$1").replace($m_jl_StackTrace$StringRE$().by("^Anonymous function\\s+", "gm"), "{anonymous}() ").replace($m_jl_StackTrace$StringRE$().by("^([^\\(]+|\\{anonymous\\}\\(\\))\\s+\\((.+)\\)$", "gm"), "$1@$2").split("\n");
  return qual$1.slice(1);
}
function $p_jl_StackTrace$__extractSafari__O__O($thiz, e) {
  return e.stack.replace($m_jl_StackTrace$StringRE$().by("\\[native code\\]\\n", "m"), "").replace($m_jl_StackTrace$StringRE$().by("^(?=\\w+Error\\:).*$\\n", "m"), "").replace($m_jl_StackTrace$StringRE$().by("^@", "gm"), "{anonymous}()@").split("\n");
}
function $p_jl_StackTrace$__extractOpera9__O__O($thiz, e) {
  var lineRE = $m_jl_StackTrace$StringRE$().by("Line (\\d+).*script (?:in )?(\\S+)", "i");
  var lines = e.message.split("\n");
  var result = [];
  var i = 2;
  var len = (lines.length | 0);
  while ((i < len)) {
    var mtch = lineRE.exec(lines[i]);
    if ((mtch !== null)) {
      (result.push(((("{anonymous}()@" + mtch[2]) + ":") + mtch[1])) | 0);
    }
    i = ((2 + i) | 0);
  }
  return result;
}
function $p_jl_StackTrace$__extractOpera10a__O__O($thiz, e) {
  var lineRE = $m_jl_StackTrace$StringRE$().by("Line (\\d+).*script (?:in )?(\\S+)(?:: In function (\\S+))?$", "i");
  var lines = e.stacktrace.split("\n");
  var result = [];
  var i = 0;
  var len = (lines.length | 0);
  while ((i < len)) {
    var mtch = lineRE.exec(lines[i]);
    if ((mtch !== null)) {
      var x = mtch[3];
      var fnName = ((x !== (void 0)) ? x : "{anonymous}");
      (result.push(((((fnName + "()@") + mtch[2]) + ":") + mtch[1])) | 0);
    }
    i = ((2 + i) | 0);
  }
  return result;
}
function $p_jl_StackTrace$__extractOpera10b__O__O($thiz, e) {
  var lineRE = $m_jl_StackTrace$StringRE$().cb("^(.*)@(.+):(\\d+)$");
  var lines = e.stacktrace.split("\n");
  var result = [];
  var i = 0;
  var len = (lines.length | 0);
  while ((i < len)) {
    var mtch = lineRE.exec(lines[i]);
    if ((mtch !== null)) {
      var x = mtch[1];
      var fnName = ((x !== (void 0)) ? (x + "()") : "global code");
      (result.push(((((fnName + "@") + mtch[2]) + ":") + mtch[3])) | 0);
    }
    i = ((1 + i) | 0);
  }
  return result;
}
function $p_jl_StackTrace$__extractOpera11__O__O($thiz, e) {
  var lineRE = $m_jl_StackTrace$StringRE$().cb("^.*line (\\d+), column (\\d+)(?: in (.+))? in (\\S+):$");
  var lines = e.stacktrace.split("\n");
  var result = [];
  var i = 0;
  var len = (lines.length | 0);
  while ((i < len)) {
    var mtch = lineRE.exec(lines[i]);
    if ((mtch !== null)) {
      var location = ((((mtch[4] + ":") + mtch[1]) + ":") + mtch[2]);
      var x$3 = mtch[2];
      var fnName0 = ((x$3 !== (void 0)) ? x$3 : "global code");
      var fnName = fnName0.replace($m_jl_StackTrace$StringRE$().cb("<anonymous function: (\\S+)>"), "$1").replace($m_jl_StackTrace$StringRE$().cb("<anonymous function>"), "{anonymous}");
      (result.push(((fnName + "@") + location)) | 0);
    }
    i = ((2 + i) | 0);
  }
  return result;
}
function $p_jl_StackTrace$__extractOther__O__O($thiz, e) {
  return [];
}
function $p_jl_StackTrace$__loop$1__I__T__T($thiz, i, encodedName$1) {
  while (true) {
    if ((i < ($p_jl_StackTrace$__compressedPrefixes__O($thiz).length | 0))) {
      var prefix = $p_jl_StackTrace$__compressedPrefixes__O($thiz)[i];
      if ((!(!encodedName$1.startsWith(prefix)))) {
        var dict = $p_jl_StackTrace$__decompressedPrefixes__O($thiz);
        return (("" + dict[prefix]) + encodedName$1.substring(prefix.length));
      } else {
        i = ((1 + i) | 0);
      }
    } else {
      return ((!(!encodedName$1.startsWith("L"))) ? encodedName$1.substring(1) : encodedName$1);
    }
  }
}
/** @constructor */
function $c_jl_StackTrace$() {
  this.i7 = null;
  this.i8 = null;
  this.i6 = null;
  this.bK = 0;
}
$p = $c_jl_StackTrace$.prototype = new $h_O();
$p.constructor = $c_jl_StackTrace$;
/** @constructor */
function $h_jl_StackTrace$() {
}
$h_jl_StackTrace$.prototype = $p;
$p.pU = (function(jsError) {
  return $p_jl_StackTrace$__normalizedLinesToStackTrace__O__Ajl_StackTraceElement(this, $p_jl_StackTrace$__normalizeStackTraceLines__O__O(this, jsError));
});
var $d_jl_StackTrace$ = new $TypeData().i($c_jl_StackTrace$, "java.lang.StackTrace$", ({
  eP: 1
}));
var $n_jl_StackTrace$;
function $m_jl_StackTrace$() {
  if ((!$n_jl_StackTrace$)) {
    $n_jl_StackTrace$ = new $c_jl_StackTrace$();
  }
  return $n_jl_StackTrace$;
}
/** @constructor */
function $c_jl_StackTrace$StringRE$() {
}
$p = $c_jl_StackTrace$StringRE$.prototype = new $h_O();
$p.constructor = $c_jl_StackTrace$StringRE$;
/** @constructor */
function $h_jl_StackTrace$StringRE$() {
}
$h_jl_StackTrace$StringRE$.prototype = $p;
$p.cb = (function(this$) {
  return new RegExp(this$);
});
$p.by = (function(this$, mods) {
  return new RegExp(this$, mods);
});
var $d_jl_StackTrace$StringRE$ = new $TypeData().i($c_jl_StackTrace$StringRE$, "java.lang.StackTrace$StringRE$", ({
  eQ: 1
}));
var $n_jl_StackTrace$StringRE$;
function $m_jl_StackTrace$StringRE$() {
  if ((!$n_jl_StackTrace$StringRE$)) {
    $n_jl_StackTrace$StringRE$ = new $c_jl_StackTrace$StringRE$();
  }
  return $n_jl_StackTrace$StringRE$;
}
/** @constructor */
function $c_jl_System$Streams$() {
  this.ev = null;
  $n_jl_System$Streams$ = this;
  this.ev = new $c_jl_JSConsoleBasedPrintStream(true);
}
$p = $c_jl_System$Streams$.prototype = new $h_O();
$p.constructor = $c_jl_System$Streams$;
/** @constructor */
function $h_jl_System$Streams$() {
}
$h_jl_System$Streams$.prototype = $p;
var $d_jl_System$Streams$ = new $TypeData().i($c_jl_System$Streams$, "java.lang.System$Streams$", ({
  eT: 1
}));
var $n_jl_System$Streams$;
function $m_jl_System$Streams$() {
  if ((!$n_jl_System$Streams$)) {
    $n_jl_System$Streams$ = new $c_jl_System$Streams$();
  }
  return $n_jl_System$Streams$;
}
function $p_jl_System$SystemProperties$__loadSystemProperties__O($thiz) {
  var result = ({});
  result["java.version"] = "1.8";
  result["java.vm.specification.version"] = "1.8";
  result["java.vm.specification.vendor"] = "Oracle Corporation";
  result["java.vm.specification.name"] = "Java Virtual Machine Specification";
  result["java.vm.name"] = "Scala.js";
  result["java.vm.version"] = "1.22.0";
  result["java.specification.version"] = "1.8";
  result["java.specification.vendor"] = "Oracle Corporation";
  result["java.specification.name"] = "Java Platform API Specification";
  result["file.separator"] = "/";
  result["path.separator"] = ":";
  result["line.separator"] = "\n";
  return result;
}
/** @constructor */
function $c_jl_System$SystemProperties$() {
  this.i9 = null;
  this.lP = null;
  $n_jl_System$SystemProperties$ = this;
  this.i9 = $p_jl_System$SystemProperties$__loadSystemProperties__O(this);
  this.lP = null;
}
$p = $c_jl_System$SystemProperties$.prototype = new $h_O();
$p.constructor = $c_jl_System$SystemProperties$;
/** @constructor */
function $h_jl_System$SystemProperties$() {
}
$h_jl_System$SystemProperties$.prototype = $p;
$p.j7 = (function(key, default$1) {
  if ((this.i9 !== null)) {
    var dict = this.i9;
    return ((!(!$m_jl_Utils$Cache$().ib.call(dict, key))) ? dict[key] : default$1);
  } else {
    return this.lP.j7(key, default$1);
  }
});
var $d_jl_System$SystemProperties$ = new $TypeData().i($c_jl_System$SystemProperties$, "java.lang.System$SystemProperties$", ({
  eU: 1
}));
var $n_jl_System$SystemProperties$;
function $m_jl_System$SystemProperties$() {
  if ((!$n_jl_System$SystemProperties$)) {
    $n_jl_System$SystemProperties$ = new $c_jl_System$SystemProperties$();
  }
  return $n_jl_System$SystemProperties$;
}
/** @constructor */
function $c_jl_ThreadLocal() {
  this.ia = false;
  this.lQ = null;
  this.ia = false;
}
$p = $c_jl_ThreadLocal.prototype = new $h_O();
$p.constructor = $c_jl_ThreadLocal;
/** @constructor */
function $h_jl_ThreadLocal() {
}
$h_jl_ThreadLocal.prototype = $p;
$p.s = (function() {
  if ((!this.ia)) {
    this.gf(null);
  }
  return this.lQ;
});
$p.gf = (function(o) {
  this.lQ = o;
  this.ia = true;
});
var $d_jl_ThreadLocal = new $TypeData().i($c_jl_ThreadLocal, "java.lang.ThreadLocal", ({
  eW: 1
}));
/** @constructor */
function $c_jl_Utils$Cache$() {
  this.ib = null;
  $n_jl_Utils$Cache$ = this;
  this.ib = Object.prototype.hasOwnProperty;
}
$p = $c_jl_Utils$Cache$.prototype = new $h_O();
$p.constructor = $c_jl_Utils$Cache$;
/** @constructor */
function $h_jl_Utils$Cache$() {
}
$h_jl_Utils$Cache$.prototype = $p;
var $d_jl_Utils$Cache$ = new $TypeData().i($c_jl_Utils$Cache$, "java.lang.Utils$Cache$", ({
  eY: 1
}));
var $n_jl_Utils$Cache$;
function $m_jl_Utils$Cache$() {
  if ((!$n_jl_Utils$Cache$)) {
    $n_jl_Utils$Cache$ = new $c_jl_Utils$Cache$();
  }
  return $n_jl_Utils$Cache$;
}
function $f_jl_Void__equals__O__Z($thiz, that) {
  return ($thiz === that);
}
function $f_jl_Void__hashCode__I($thiz) {
  return 0;
}
function $f_jl_Void__toString__T($thiz) {
  return "undefined";
}
function $isArrayOf_jl_Void(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.bD)));
}
var $d_jl_Void = new $TypeData().i(0, "java.lang.Void", ({
  bD: 1
}), ((x) => (x === (void 0))));
function $p_jl_reflect_Array$__mismatch__O__E($thiz, array) {
  throw $ct_jl_IllegalArgumentException__T__(new $c_jl_IllegalArgumentException(), "argument type mismatch");
}
/** @constructor */
function $c_jl_reflect_Array$() {
}
$p = $c_jl_reflect_Array$.prototype = new $h_O();
$p.constructor = $c_jl_reflect_Array$;
/** @constructor */
function $h_jl_reflect_Array$() {
}
$h_jl_reflect_Array$.prototype = $p;
$p.bJ = (function(array) {
  if ((array instanceof $ac_O)) {
    return array.a.length;
  } else if ((array instanceof $ac_Z)) {
    return array.a.length;
  } else if ((array instanceof $ac_C)) {
    return array.a.length;
  } else if ((array instanceof $ac_B)) {
    return array.a.length;
  } else if ((array instanceof $ac_S)) {
    return array.a.length;
  } else if ((array instanceof $ac_I)) {
    return array.a.length;
  } else if ((array instanceof $ac_J)) {
    return ((array.a.length >>> 1) | 0);
  } else if ((array instanceof $ac_F)) {
    return array.a.length;
  } else {
    if ((!(array instanceof $ac_D))) {
      $p_jl_reflect_Array$__mismatch__O__E(this, array);
    }
    return array.a.length;
  }
});
var $d_jl_reflect_Array$ = new $TypeData().i($c_jl_reflect_Array$, "java.lang.reflect.Array$", ({
  eZ: 1
}));
var $n_jl_reflect_Array$;
function $m_jl_reflect_Array$() {
  if ((!$n_jl_reflect_Array$)) {
    $n_jl_reflect_Array$ = new $c_jl_reflect_Array$();
  }
  return $n_jl_reflect_Array$;
}
/** @constructor */
function $c_ju_Arrays$() {
}
$p = $c_ju_Arrays$.prototype = new $h_O();
$p.constructor = $c_ju_Arrays$;
/** @constructor */
function $h_ju_Arrays$() {
}
$h_ju_Arrays$.prototype = $p;
$p.pk = (function(a, key) {
  var startIndex = 0;
  var endIndex = a.a.length;
  while (true) {
    if ((startIndex === endIndex)) {
      return (~startIndex);
    } else {
      var mid = ((((startIndex + endIndex) | 0) >>> 1) | 0);
      var elem = a.a[mid];
      var cmp = ((key === elem) ? 0 : ((key < elem) ? (-1) : 1));
      if ((cmp < 0)) {
        endIndex = mid;
        continue;
      }
      if ((cmp !== 0)) {
        startIndex = ((1 + mid) | 0);
        continue;
      }
      return mid;
    }
  }
});
$p.nq = (function(a, b) {
  if ((a === b)) {
    return true;
  }
  if (((a === null) || (b === null))) {
    return false;
  }
  var len = ((a.a.length >>> 1) | 0);
  if ((((b.a.length >>> 1) | 0) !== len)) {
    return false;
  }
  var i = 0;
  while ((i !== len)) {
    var i$1 = i;
    var $x_1 = a.a;
    var $x_2 = (i$1 << 1);
    var a$1_$_lo = $x_1[$x_2];
    var a$1_$_hi = $x_1[(($x_2 + 1) | 0)];
    var i$2 = i;
    var $x_3 = b.a;
    var $x_4 = (i$2 << 1);
    var b$1_$_lo = $x_3[$x_4];
    var b$1_$_hi = $x_3[(($x_4 + 1) | 0)];
    if ((!(((a$1_$_lo ^ b$1_$_lo) | (a$1_$_hi ^ b$1_$_hi)) === 0))) {
      return false;
    }
    i = ((1 + i) | 0);
  }
  return true;
});
$p.iU = (function(a, b) {
  if ((a === b)) {
    return true;
  }
  if (((a === null) || (b === null))) {
    return false;
  }
  var len = a.a.length;
  if ((b.a.length !== len)) {
    return false;
  }
  var i = 0;
  while ((i !== len)) {
    var i$1 = i;
    var $x_1 = a.a[i$1];
    var i$2 = i;
    if ((!($x_1 === b.a[i$2]))) {
      return false;
    }
    i = ((1 + i) | 0);
  }
  return true;
});
$p.nr = (function(a, b) {
  if ((a === b)) {
    return true;
  }
  if (((a === null) || (b === null))) {
    return false;
  }
  var len = a.a.length;
  if ((b.a.length !== len)) {
    return false;
  }
  var i = 0;
  while ((i !== len)) {
    var i$1 = i;
    var $x_1 = a.a[i$1];
    var i$2 = i;
    if ((!($x_1 === b.a[i$2]))) {
      return false;
    }
    i = ((1 + i) | 0);
  }
  return true;
});
$p.np = (function(a, b) {
  if ((a === b)) {
    return true;
  }
  if (((a === null) || (b === null))) {
    return false;
  }
  var len = a.a.length;
  if ((b.a.length !== len)) {
    return false;
  }
  var i = 0;
  while ((i !== len)) {
    var i$1 = i;
    var $x_1 = a.a[i$1];
    var i$2 = i;
    if ((!($x_1 === b.a[i$2]))) {
      return false;
    }
    i = ((1 + i) | 0);
  }
  return true;
});
$p.no = (function(a, b) {
  if ((a === b)) {
    return true;
  }
  if (((a === null) || (b === null))) {
    return false;
  }
  var len = a.a.length;
  if ((b.a.length !== len)) {
    return false;
  }
  var i = 0;
  while ((i !== len)) {
    var i$1 = i;
    var $x_1 = a.a[i$1];
    var i$2 = i;
    if ((!($x_1 === b.a[i$2]))) {
      return false;
    }
    i = ((1 + i) | 0);
  }
  return true;
});
$p.ns = (function(a, b) {
  if ((a === b)) {
    return true;
  }
  if (((a === null) || (b === null))) {
    return false;
  }
  var len = a.a.length;
  if ((b.a.length !== len)) {
    return false;
  }
  var i = 0;
  while ((i !== len)) {
    var i$1 = i;
    var $x_1 = a.a[i$1];
    var i$2 = i;
    if ((!($x_1 === b.a[i$2]))) {
      return false;
    }
    i = ((1 + i) | 0);
  }
  return true;
});
$p.S = (function(original, newLength) {
  var b = original.a.length;
  var copyLength = ((newLength < b) ? newLength : b);
  var ret = $objectGetClass(original).ah.Q().ah.U(newLength);
  original.u(0, ret, 0, copyLength);
  return ret;
});
$p.Z = (function(original, from, to) {
  if ((from > to)) {
    throw $ct_jl_IllegalArgumentException__T__(new $c_jl_IllegalArgumentException(), ((from + " > ") + to));
  }
  var len = original.a.length;
  var retLength = ((to - from) | 0);
  var b = ((len - from) | 0);
  var copyLength = ((retLength < b) ? retLength : b);
  var ret = $objectGetClass(original).ah.Q().ah.U(retLength);
  original.u(from, ret, 0, copyLength);
  return ret;
});
var $d_ju_Arrays$ = new $TypeData().i($c_ju_Arrays$, "java.util.Arrays$", ({
  f0: 1
}));
var $n_ju_Arrays$;
function $m_ju_Arrays$() {
  if ((!$n_ju_Arrays$)) {
    $n_ju_Arrays$ = new $c_ju_Arrays$();
  }
  return $n_ju_Arrays$;
}
function $s_RTLong__remainderUnsigned__I__I__I__I__J(alo, ahi, blo, bhi) {
  return $m_RTLong$().qV(alo, ahi, blo, bhi);
}
function $s_RTLong__remainder__I__I__I__I__J(alo, ahi, blo, bhi) {
  return $m_RTLong$().qU(alo, ahi, blo, bhi);
}
function $s_RTLong__divideUnsigned__I__I__I__I__J(alo, ahi, blo, bhi) {
  return $m_RTLong$().pM(alo, ahi, blo, bhi);
}
function $s_RTLong__divide__I__I__I__I__J(alo, ahi, blo, bhi) {
  return $m_RTLong$().pL(alo, ahi, blo, bhi);
}
function $s_RTLong__fromDoubleBits__D__O__J(value, fpBitsDataView) {
  fpBitsDataView.setFloat64(0, value, true);
  var lo = (fpBitsDataView.getInt32(0, true) | 0);
  var hi = (fpBitsDataView.getInt32(4, true) | 0);
  return $bL(lo, hi);
}
function $s_RTLong__fromDouble__D__J(value) {
  return $m_RTLong$().h6(value);
}
function $s_RTLong__fromUnsignedInt__I__J(value) {
  return $bL(value, 0);
}
function $s_RTLong__fromInt__I__J(value) {
  var hi = (value >> 31);
  return $bL(value, hi);
}
function $s_RTLong__clz__I__I__I(lo, hi) {
  return ((hi !== 0) ? Math.clz32(hi) : ((32 + Math.clz32(lo)) | 0));
}
function $s_RTLong__toFloat__I__I__F(lo, hi) {
  return Math.fround(((4.294967296E9 * hi) + ((((((-2097152) & (hi ^ (hi >> 10))) === 0) || ((65535 & lo) === 0)) ? lo : (32768 | ((-32768) & lo))) >>> 0.0)));
}
function $s_RTLong__toDouble__I__I__D(lo, hi) {
  return ((4.294967296E9 * hi) + (lo >>> 0.0));
}
function $s_RTLong__toInt__I__I__I(lo, hi) {
  return lo;
}
function $s_RTLong__toString__I__I__T(lo, hi) {
  return $m_RTLong$().oi(lo, hi);
}
function $s_RTLong__bitsToDouble__I__I__O__D(lo, hi, fpBitsDataView) {
  fpBitsDataView.setInt32(0, lo, true);
  fpBitsDataView.setInt32(4, hi, true);
  return (+fpBitsDataView.getFloat64(0, true));
}
function $s_RTLong__mul__I__I__I__I__J(alo, ahi, blo, bhi) {
  var a0 = (65535 & alo);
  var a1 = ((alo >>> 16) | 0);
  var b0 = (65535 & blo);
  var b1 = ((blo >>> 16) | 0);
  var a0b0 = Math.imul(a0, b0);
  var a1b0 = Math.imul(a1, b0);
  var a0b1 = Math.imul(a0, b1);
  var lo = ((a0b0 + (((a1b0 + a0b1) | 0) << 16)) | 0);
  var c1part = ((((a0b0 >>> 16) | 0) + a0b1) | 0);
  var hi = ((((((((Math.imul(alo, bhi) + Math.imul(ahi, blo)) | 0) + Math.imul(a1, b1)) | 0) + ((c1part >>> 16) | 0)) | 0) + (((((65535 & c1part) + a1b0) | 0) >>> 16) | 0)) | 0);
  return $bL(lo, hi);
}
function $s_RTLong__sub__I__I__I__I__J(alo, ahi, blo, bhi) {
  var lo = ((alo - blo) | 0);
  var hi = ((((ahi - bhi) | 0) - (((lo >>> 0) > (alo >>> 0)) | 0)) | 0);
  return $bL(lo, hi);
}
function $s_RTLong__add__I__I__I__I__J(alo, ahi, blo, bhi) {
  var lo = ((alo + blo) | 0);
  var hi = ((((ahi + bhi) | 0) + (((lo >>> 0) < (alo >>> 0)) | 0)) | 0);
  return $bL(lo, hi);
}
function $s_RTLong__sar__I__I__I__J(lo, hi, n) {
  var lo$1 = (((32 & n) === 0) ? (((lo >>> n) | 0) | ((hi << 1) << (~n))) : (hi >> n));
  var hi$1 = (((32 & n) === 0) ? (hi >> n) : (hi >> 31));
  return $bL(lo$1, hi$1);
}
function $s_RTLong__shr__I__I__I__J(lo, hi, n) {
  var lo$1 = (((32 & n) === 0) ? (((lo >>> n) | 0) | ((hi << 1) << (~n))) : ((hi >>> n) | 0));
  var hi$1 = (((32 & n) === 0) ? ((hi >>> n) | 0) : 0);
  return $bL(lo$1, hi$1);
}
function $s_RTLong__shl__I__I__I__J(lo, hi, n) {
  var lo$1 = (((32 & n) === 0) ? (lo << n) : 0);
  var hi$1 = (((32 & n) === 0) ? (((((lo >>> 1) | 0) >>> (~n)) | 0) | (hi << n)) : (lo << n));
  return $bL(lo$1, hi$1);
}
function $s_RTLong__xor__I__I__I__I__J(alo, ahi, blo, bhi) {
  var lo = (alo ^ blo);
  var hi = (ahi ^ bhi);
  return $bL(lo, hi);
}
function $s_RTLong__and__I__I__I__I__J(alo, ahi, blo, bhi) {
  var lo = (alo & blo);
  var hi = (ahi & bhi);
  return $bL(lo, hi);
}
function $s_RTLong__or__I__I__I__I__J(alo, ahi, blo, bhi) {
  var lo = (alo | blo);
  var hi = (ahi | bhi);
  return $bL(lo, hi);
}
function $s_RTLong__geu__I__I__I__I__Z(alo, ahi, blo, bhi) {
  return ((ahi === bhi) ? ((alo >>> 0) >= (blo >>> 0)) : ((ahi >>> 0) > (bhi >>> 0)));
}
function $s_RTLong__gtu__I__I__I__I__Z(alo, ahi, blo, bhi) {
  return ((ahi === bhi) ? ((alo >>> 0) > (blo >>> 0)) : ((ahi >>> 0) > (bhi >>> 0)));
}
function $s_RTLong__leu__I__I__I__I__Z(alo, ahi, blo, bhi) {
  return ((ahi === bhi) ? ((alo >>> 0) <= (blo >>> 0)) : ((ahi >>> 0) < (bhi >>> 0)));
}
function $s_RTLong__ltu__I__I__I__I__Z(alo, ahi, blo, bhi) {
  return ((ahi === bhi) ? ((alo >>> 0) < (blo >>> 0)) : ((ahi >>> 0) < (bhi >>> 0)));
}
function $s_RTLong__ge__I__I__I__I__Z(alo, ahi, blo, bhi) {
  return ((ahi === bhi) ? ((alo >>> 0) >= (blo >>> 0)) : (ahi > bhi));
}
function $s_RTLong__gt__I__I__I__I__Z(alo, ahi, blo, bhi) {
  return ((ahi === bhi) ? ((alo >>> 0) > (blo >>> 0)) : (ahi > bhi));
}
function $s_RTLong__le__I__I__I__I__Z(alo, ahi, blo, bhi) {
  return ((ahi === bhi) ? ((alo >>> 0) <= (blo >>> 0)) : (ahi < bhi));
}
function $s_RTLong__lt__I__I__I__I__Z(alo, ahi, blo, bhi) {
  return ((ahi === bhi) ? ((alo >>> 0) < (blo >>> 0)) : (ahi < bhi));
}
function $s_RTLong__notEquals__I__I__I__I__Z(alo, ahi, blo, bhi) {
  return (((alo ^ blo) | (ahi ^ bhi)) !== 0);
}
function $s_RTLong__equals__I__I__I__I__Z(alo, ahi, blo, bhi) {
  return (((alo ^ blo) | (ahi ^ bhi)) === 0);
}
/** @constructor */
function $c_RTLong$() {
}
$p = $c_RTLong$.prototype = new $h_O();
$p.constructor = $c_RTLong$;
/** @constructor */
function $h_RTLong$() {
}
$h_RTLong$.prototype = $p;
$p.oi = (function(lo, hi) {
  if ((hi === (lo >> 31))) {
    return ("" + lo);
  } else if ((((-2097152) & (hi ^ (hi >> 10))) === 0)) {
    return ("" + ((4.294967296E9 * hi) + (lo >>> 0.0)));
  } else {
    var sign = (hi >> 31);
    var xlo = (lo ^ sign);
    var rlo = ((xlo - sign) | 0);
    var rhi = (((hi ^ sign) + (((rlo >>> 0) < (xlo >>> 0)) | 0)) | 0);
    var aHat = ((4.294967296E9 * (rhi >>> 0.0)) + (rlo >>> 0.0));
    var qHat = (+Math.floor((1.0000000000000265E-9 * aHat)));
    var rHat = ((rlo - Math.imul(1000000000, (qHat | 0.0))) | 0);
    if ((rHat < 0)) {
      qHat = (qHat - 1.0);
      rHat = ((1000000000 + rHat) | 0);
    }
    var this$7 = rHat;
    var remStr = ("" + this$7);
    var $x_1 = qHat;
    var start = remStr.length;
    var s = ((("" + $x_1) + "000000000".substring(start)) + remStr);
    return ((hi < 0) ? ("-" + s) : s);
  }
});
$p.h6 = (function(value) {
  if ((value < (-9.223372036854776E18))) {
    return $bL(0, (-2147483648));
  } else if ((value >= 9.223372036854776E18)) {
    return $bL((-1), 2147483647);
  } else {
    var rawLo = (value | 0.0);
    var rawHi = ((2.3283064365386963E-10 * value) | 0.0);
    var hi = (((value < 0.0) && (rawLo !== 0)) ? ((rawHi - 1) | 0) : rawHi);
    return $bL(rawLo, hi);
  }
});
$p.pL = (function(alo, ahi, blo, bhi) {
  var sign = (ahi >> 31);
  var xlo = (alo ^ sign);
  var rlo = ((xlo - sign) | 0);
  var rhi = (((ahi ^ sign) + (((rlo >>> 0) < (xlo >>> 0)) | 0)) | 0);
  var sign$1 = (bhi >> 31);
  var xlo$1 = (blo ^ sign$1);
  var rlo$1 = ((xlo$1 - sign$1) | 0);
  var rhi$1 = (((bhi ^ sign$1) + (((rlo$1 >>> 0) < (xlo$1 >>> 0)) | 0)) | 0);
  if (((rhi$1 | ((-2097152) & rlo$1)) === 0)) {
    var quotHi = (((rhi >>> 0) / ($checkIntDivisor(rlo$1) >>> 0)) | 0);
    var k = ((rhi - Math.imul(rlo$1, quotHi)) | 0);
    var quotLo = ((((4.294967296E9 * k) + (rlo >>> 0.0)) / rlo$1) | 0.0);
    var absR_$_lo = quotLo;
    var absR_$_hi = quotHi;
  } else {
    var aHat = ((4.294967296E9 * (rhi >>> 0.0)) + (rlo >>> 0.0));
    var bHat = ((4.294967296E9 * (rhi$1 >>> 0.0)) + (rlo$1 >>> 0.0));
    var x$1 = ((aHat / bHat) + 0.00390625);
    var lo = (x$1 | 0.0);
    var hi = ((2.3283064365386963E-10 * x$1) | 0.0);
    var a0 = (65535 & rlo$1);
    var a1 = ((rlo$1 >>> 16) | 0);
    var b0 = (65535 & lo);
    var b1 = ((lo >>> 16) | 0);
    var a0b0 = Math.imul(a0, b0);
    var a1b0 = Math.imul(a1, b0);
    var a0b1 = Math.imul(a0, b1);
    var lo$1 = ((a0b0 + (((a1b0 + a0b1) | 0) << 16)) | 0);
    var c1part = ((((a0b0 >>> 16) | 0) + a0b1) | 0);
    if ((((((rhi - ((((((((Math.imul(rlo$1, hi) + Math.imul(rhi$1, lo)) | 0) + Math.imul(a1, b1)) | 0) + ((c1part >>> 16) | 0)) | 0) + (((((65535 & c1part) + a1b0) | 0) >>> 16) | 0)) | 0)) | 0) - (((((rlo - lo$1) | 0) >>> 0) > (rlo >>> 0)) | 0)) | 0) < 0)) {
      var lo$3 = ((lo - 1) | 0);
      var hi$3 = ((((hi - 1) | 0) + ((lo$3 !== (-1)) | 0)) | 0);
      var absR_$_lo = lo$3;
      var absR_$_hi = hi$3;
    } else {
      var absR_$_lo = lo;
      var absR_$_hi = hi;
    }
  }
  if (((ahi ^ bhi) >= 0)) {
    return $bL(absR_$_lo, absR_$_hi);
  } else {
    var lo$4 = ((-absR_$_lo) | 0);
    var hi$4 = ((((-absR_$_hi) | 0) - ((lo$4 !== 0) | 0)) | 0);
    return $bL(lo$4, hi$4);
  }
});
$p.pM = (function(alo, ahi, blo, bhi) {
  if (((bhi | ((-2097152) & blo)) === 0)) {
    var quotHi = (((ahi >>> 0) / ($checkIntDivisor(blo) >>> 0)) | 0);
    var k = ((ahi - Math.imul(blo, quotHi)) | 0);
    var quotLo = ((((4.294967296E9 * k) + (alo >>> 0.0)) / blo) | 0.0);
    return $bL(quotLo, quotHi);
  } else if ((bhi >= 0)) {
    var aHat = ((4.294967296E9 * (ahi >>> 0.0)) + (alo >>> 0.0));
    var bHat = ((4.294967296E9 * (bhi >>> 0.0)) + (blo >>> 0.0));
    var x$1 = ((aHat / bHat) + 0.00390625);
    var lo = (x$1 | 0.0);
    var hi = ((2.3283064365386963E-10 * x$1) | 0.0);
    var a0 = (65535 & blo);
    var a1 = ((blo >>> 16) | 0);
    var b0 = (65535 & lo);
    var b1 = ((lo >>> 16) | 0);
    var a0b0 = Math.imul(a0, b0);
    var a1b0 = Math.imul(a1, b0);
    var a0b1 = Math.imul(a0, b1);
    var lo$1 = ((a0b0 + (((a1b0 + a0b1) | 0) << 16)) | 0);
    var c1part = ((((a0b0 >>> 16) | 0) + a0b1) | 0);
    if ((((((ahi - ((((((((Math.imul(blo, hi) + Math.imul(bhi, lo)) | 0) + Math.imul(a1, b1)) | 0) + ((c1part >>> 16) | 0)) | 0) + (((((65535 & c1part) + a1b0) | 0) >>> 16) | 0)) | 0)) | 0) - (((((alo - lo$1) | 0) >>> 0) > (alo >>> 0)) | 0)) | 0) < 0)) {
      var lo$3 = ((lo - 1) | 0);
      var hi$3 = ((((hi - 1) | 0) + ((lo$3 !== (-1)) | 0)) | 0);
      return $bL(lo$3, hi$3);
    } else {
      return $bL(lo, hi);
    }
  } else if (((ahi === bhi) ? ((alo >>> 0) < (blo >>> 0)) : ((ahi >>> 0) < (bhi >>> 0)))) {
    return $bL(0, 0);
  } else {
    return $bL(1, 0);
  }
});
$p.qU = (function(alo, ahi, blo, bhi) {
  var sign = (ahi >> 31);
  var xlo = (alo ^ sign);
  var rlo = ((xlo - sign) | 0);
  var rhi = (((ahi ^ sign) + (((rlo >>> 0) < (xlo >>> 0)) | 0)) | 0);
  var sign$1 = (bhi >> 31);
  var xlo$1 = (blo ^ sign$1);
  var rlo$1 = ((xlo$1 - sign$1) | 0);
  var rhi$1 = (((bhi ^ sign$1) + (((rlo$1 >>> 0) < (xlo$1 >>> 0)) | 0)) | 0);
  if (((rhi$1 | ((-2097152) & rlo$1)) === 0)) {
    var k$2 = (((rhi >>> 0) % ($checkIntDivisor(rlo$1) >>> 0)) | 0);
    var quotLo$2 = ((((4.294967296E9 * k$2) + (rlo >>> 0.0)) / rlo$1) | 0.0);
    var remLo = ((rlo - Math.imul(rlo$1, quotLo$2)) | 0);
    var absR_$_lo = remLo;
    var absR_$_hi = 0;
  } else {
    var aHat = ((4.294967296E9 * (rhi >>> 0.0)) + (rlo >>> 0.0));
    var bHat = ((4.294967296E9 * (rhi$1 >>> 0.0)) + (rlo$1 >>> 0.0));
    var x$1 = ((aHat / bHat) + 0.00390625);
    var lo = (x$1 | 0.0);
    var hi = ((2.3283064365386963E-10 * x$1) | 0.0);
    var a0 = (65535 & rlo$1);
    var a1 = ((rlo$1 >>> 16) | 0);
    var b0 = (65535 & lo);
    var b1 = ((lo >>> 16) | 0);
    var a0b0 = Math.imul(a0, b0);
    var a1b0 = Math.imul(a1, b0);
    var a0b1 = Math.imul(a0, b1);
    var lo$1 = ((a0b0 + (((a1b0 + a0b1) | 0) << 16)) | 0);
    var c1part = ((((a0b0 >>> 16) | 0) + a0b1) | 0);
    var hi$1 = ((((((((Math.imul(rlo$1, hi) + Math.imul(rhi$1, lo)) | 0) + Math.imul(a1, b1)) | 0) + ((c1part >>> 16) | 0)) | 0) + (((((65535 & c1part) + a1b0) | 0) >>> 16) | 0)) | 0);
    var lo$2 = ((rlo - lo$1) | 0);
    var hi$2 = ((((rhi - hi$1) | 0) - (((lo$2 >>> 0) > (rlo >>> 0)) | 0)) | 0);
    if ((hi$2 < 0)) {
      var lo$3 = ((lo$2 + rlo$1) | 0);
      var hi$3 = ((((hi$2 + rhi$1) | 0) + (((lo$3 >>> 0) < (lo$2 >>> 0)) | 0)) | 0);
      var absR_$_lo = lo$3;
      var absR_$_hi = hi$3;
    } else {
      var absR_$_lo = lo$2;
      var absR_$_hi = hi$2;
    }
  }
  if ((ahi < 0)) {
    var lo$4 = ((-absR_$_lo) | 0);
    var hi$4 = ((((-absR_$_hi) | 0) - ((lo$4 !== 0) | 0)) | 0);
    return $bL(lo$4, hi$4);
  } else {
    return $bL(absR_$_lo, absR_$_hi);
  }
});
$p.qV = (function(alo, ahi, blo, bhi) {
  if (((bhi | ((-2097152) & blo)) === 0)) {
    var k$2 = (((ahi >>> 0) % ($checkIntDivisor(blo) >>> 0)) | 0);
    var quotLo$2 = ((((4.294967296E9 * k$2) + (alo >>> 0.0)) / blo) | 0.0);
    var remLo = ((alo - Math.imul(blo, quotLo$2)) | 0);
    return $bL(remLo, 0);
  } else if ((bhi >= 0)) {
    var aHat = ((4.294967296E9 * (ahi >>> 0.0)) + (alo >>> 0.0));
    var bHat = ((4.294967296E9 * (bhi >>> 0.0)) + (blo >>> 0.0));
    var x$1 = ((aHat / bHat) + 0.00390625);
    var lo = (x$1 | 0.0);
    var hi = ((2.3283064365386963E-10 * x$1) | 0.0);
    var a0 = (65535 & blo);
    var a1 = ((blo >>> 16) | 0);
    var b0 = (65535 & lo);
    var b1 = ((lo >>> 16) | 0);
    var a0b0 = Math.imul(a0, b0);
    var a1b0 = Math.imul(a1, b0);
    var a0b1 = Math.imul(a0, b1);
    var lo$1 = ((a0b0 + (((a1b0 + a0b1) | 0) << 16)) | 0);
    var c1part = ((((a0b0 >>> 16) | 0) + a0b1) | 0);
    var hi$1 = ((((((((Math.imul(blo, hi) + Math.imul(bhi, lo)) | 0) + Math.imul(a1, b1)) | 0) + ((c1part >>> 16) | 0)) | 0) + (((((65535 & c1part) + a1b0) | 0) >>> 16) | 0)) | 0);
    var lo$2 = ((alo - lo$1) | 0);
    var hi$2 = ((((ahi - hi$1) | 0) - (((lo$2 >>> 0) > (alo >>> 0)) | 0)) | 0);
    if ((hi$2 < 0)) {
      var lo$3 = ((lo$2 + blo) | 0);
      var hi$3 = ((((hi$2 + bhi) | 0) + (((lo$3 >>> 0) < (lo$2 >>> 0)) | 0)) | 0);
      return $bL(lo$3, hi$3);
    } else {
      return $bL(lo$2, hi$2);
    }
  } else if (((ahi === bhi) ? ((alo >>> 0) < (blo >>> 0)) : ((ahi >>> 0) < (bhi >>> 0)))) {
    return $bL(alo, ahi);
  } else {
    var lo$4 = ((alo - blo) | 0);
    var hi$4 = ((((ahi - bhi) | 0) - (((lo$4 >>> 0) > (alo >>> 0)) | 0)) | 0);
    return $bL(lo$4, hi$4);
  }
});
var $d_RTLong$ = new $TypeData().i($c_RTLong$, "org.scalajs.linker.runtime.RuntimeLong$", ({
  f3: 1
}));
var $n_RTLong$;
function $m_RTLong$() {
  if ((!$n_RTLong$)) {
    $n_RTLong$ = new $c_RTLong$();
  }
  return $n_RTLong$;
}
function $p_s_Array$__slowcopy__O__I__O__I__I__V($thiz, src, srcPos, dest, destPos, length) {
  var i = srcPos;
  var j = destPos;
  var srcUntil = ((srcPos + length) | 0);
  while ((i < srcUntil)) {
    $m_sr_ScalaRunTime$().gY(dest, j, $m_sr_ScalaRunTime$().dZ(src, i));
    i = ((1 + i) | 0);
    j = ((1 + j) | 0);
  }
}
/** @constructor */
function $c_s_Array$() {
}
$p = $c_s_Array$.prototype = new $h_O();
$p.constructor = $c_s_Array$;
/** @constructor */
function $h_s_Array$() {
}
$h_s_Array$.prototype = $p;
$p.nu = (function(it, evidence$1) {
  var n = it.x();
  if ((n > (-1))) {
    var elements = evidence$1.bo(n);
    var iterator = it.i();
    var i = 0;
    while ((i < n)) {
      $m_sr_ScalaRunTime$().gY(elements, i, iterator.g());
      i = ((1 + i) | 0);
    }
    return elements;
  } else {
    var capacity = 0;
    var size = 0;
    var jsElems = null;
    var elementClass = evidence$1.aC();
    capacity = 0;
    size = 0;
    var isCharArrayBuilder = (elementClass === $d_C.l());
    jsElems = [];
    var iterator$2 = it.i();
    while (iterator$2.m()) {
      var elem = iterator$2.g();
      var unboxedElem = (isCharArrayBuilder ? $uC(elem) : ((elem === null) ? $m_scm_ArrayBuilder$().hk(elementClass) : elem));
      jsElems.push(unboxedElem);
    }
    return $m_scm_ArrayBuilder$().hj(((elementClass === $d_V.l()) ? $d_jl_Void.l() : (((elementClass === $d_sr_Null$.l()) || (elementClass === $d_sr_Nothing$.l())) ? $d_O.l() : elementClass)), jsElems);
  }
});
$p.fZ = (function(src, srcPos, dest, destPos, length) {
  var srcClass = $objectGetClass(src);
  if ((srcClass.ah.Z && $objectGetClass(dest).ah.R(srcClass.ah))) {
    src.u(srcPos, dest, destPos, length);
  } else {
    $p_s_Array$__slowcopy__O__I__O__I__I__V(this, src, srcPos, dest, destPos, length);
  }
});
$p.nt = (function(xs, ys) {
  if ((xs === ys)) {
    return true;
  }
  if ((xs.a.length !== ys.a.length)) {
    return false;
  }
  var len = xs.a.length;
  var i = 0;
  while ((i < len)) {
    if ((!$m_sr_BoxesRunTime$().j(xs.a[i], ys.a[i]))) {
      return false;
    }
    i = ((1 + i) | 0);
  }
  return true;
});
var $d_s_Array$ = new $TypeData().i($c_s_Array$, "scala.Array$", ({
  f4: 1
}));
var $n_s_Array$;
function $m_s_Array$() {
  if ((!$n_s_Array$)) {
    $n_s_Array$ = new $c_s_Array$();
  }
  return $n_s_Array$;
}
/** @constructor */
function $c_s_Array$EmptyArrays$() {
  this.ic = null;
  this.lU = null;
  $n_s_Array$EmptyArrays$ = this;
  this.ic = new $ac_I(0);
  this.lU = new $ac_O(0);
}
$p = $c_s_Array$EmptyArrays$.prototype = new $h_O();
$p.constructor = $c_s_Array$EmptyArrays$;
/** @constructor */
function $h_s_Array$EmptyArrays$() {
}
$h_s_Array$EmptyArrays$.prototype = $p;
var $d_s_Array$EmptyArrays$ = new $TypeData().i($c_s_Array$EmptyArrays$, "scala.Array$EmptyArrays$", ({
  f5: 1
}));
var $n_s_Array$EmptyArrays$;
function $m_s_Array$EmptyArrays$() {
  if ((!$n_s_Array$EmptyArrays$)) {
    $n_s_Array$EmptyArrays$ = new $c_s_Array$EmptyArrays$();
  }
  return $n_s_Array$EmptyArrays$;
}
var $d_F0 = new $TypeData().i(1, "scala.Function0", ({
  aH: 1
}));
var $d_F1 = new $TypeData().i(1, "scala.Function1", ({
  e: 1
}));
/** @constructor */
function $c_s_LowPriorityImplicits2() {
}
$p = $c_s_LowPriorityImplicits2.prototype = new $h_O();
$p.constructor = $c_s_LowPriorityImplicits2;
/** @constructor */
function $h_s_LowPriorityImplicits2() {
}
$h_s_LowPriorityImplicits2.prototype = $p;
/** @constructor */
function $c_s_Option$() {
}
$p = $c_s_Option$.prototype = new $h_O();
$p.constructor = $c_s_Option$;
/** @constructor */
function $h_s_Option$() {
}
$h_s_Option$.prototype = $p;
$p.n9 = (function(x) {
  return ((x === null) ? $m_s_None$() : new $c_s_Some(x));
});
var $d_s_Option$ = new $TypeData().i($c_s_Option$, "scala.Option$", ({
  fc: 1
}));
var $n_s_Option$;
function $m_s_Option$() {
  if ((!$n_s_Option$)) {
    $n_s_Option$ = new $c_s_Option$();
  }
  return $n_s_Option$;
}
/** @constructor */
function $c_s_PartialFunction$() {
  this.lX = null;
  this.gC = null;
  $n_s_PartialFunction$ = this;
  this.lX = new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((_$2$2) => this.lX));
  this.gC = new $c_s_PartialFunction$$anon$1();
}
$p = $c_s_PartialFunction$.prototype = new $h_O();
$p.constructor = $c_s_PartialFunction$;
/** @constructor */
function $h_s_PartialFunction$() {
}
$h_s_PartialFunction$.prototype = $p;
var $d_s_PartialFunction$ = new $TypeData().i($c_s_PartialFunction$, "scala.PartialFunction$", ({
  fd: 1
}));
var $n_s_PartialFunction$;
function $m_s_PartialFunction$() {
  if ((!$n_s_PartialFunction$)) {
    $n_s_PartialFunction$ = new $c_s_PartialFunction$();
  }
  return $n_s_PartialFunction$;
}
/** @constructor */
function $c_sc_ArrayOps$() {
  this.m0 = null;
  $n_sc_ArrayOps$ = this;
  this.m0 = new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((x$1$2$2) => $m_sc_ArrayOps$().m0));
}
$p = $c_sc_ArrayOps$.prototype = new $h_O();
$p.constructor = $c_sc_ArrayOps$;
/** @constructor */
function $h_sc_ArrayOps$() {
}
$h_sc_ArrayOps$.prototype = $p;
$p.q0 = (function(this$, f) {
  var len = $m_jl_reflect_Array$().bJ(this$);
  var i = 0;
  if ((this$ instanceof $ac_O)) {
    while ((i < len)) {
      f.b(this$.a[i]);
      i = ((1 + i) | 0);
    }
  } else if ((this$ instanceof $ac_I)) {
    while ((i < len)) {
      f.b(this$.a[i]);
      i = ((1 + i) | 0);
    }
  } else if ((this$ instanceof $ac_D)) {
    while ((i < len)) {
      f.b(this$.a[i]);
      i = ((1 + i) | 0);
    }
  } else if ((this$ instanceof $ac_J)) {
    while ((i < len)) {
      var $x_2 = this$.a;
      var $x_3 = (i << 1);
      var $x_1_$_lo = $x_2[$x_3];
      var $x_1_$_hi = $x_2[(($x_3 + 1) | 0)];
      f.b($bL($x_1_$_lo, $x_1_$_hi));
      i = ((1 + i) | 0);
    }
  } else if ((this$ instanceof $ac_F)) {
    while ((i < len)) {
      f.b(this$.a[i]);
      i = ((1 + i) | 0);
    }
  } else if ((this$ instanceof $ac_C)) {
    while ((i < len)) {
      f.b($bC(this$.a[i]));
      i = ((1 + i) | 0);
    }
  } else if ((this$ instanceof $ac_B)) {
    while ((i < len)) {
      f.b(this$.a[i]);
      i = ((1 + i) | 0);
    }
  } else if ((this$ instanceof $ac_S)) {
    while ((i < len)) {
      f.b(this$.a[i]);
      i = ((1 + i) | 0);
    }
  } else if ((this$ instanceof $ac_Z)) {
    while ((i < len)) {
      f.b(this$.a[i]);
      i = ((1 + i) | 0);
    }
  } else {
    throw new $c_s_MatchError(this$);
  }
});
var $d_sc_ArrayOps$ = new $TypeData().i($c_sc_ArrayOps$, "scala.collection.ArrayOps$", ({
  fk: 1
}));
var $n_sc_ArrayOps$;
function $m_sc_ArrayOps$() {
  if ((!$n_sc_ArrayOps$)) {
    $n_sc_ArrayOps$ = new $c_sc_ArrayOps$();
  }
  return $n_sc_ArrayOps$;
}
/** @constructor */
function $c_sc_Hashing$() {
}
$p = $c_sc_Hashing$.prototype = new $h_O();
$p.constructor = $c_sc_Hashing$;
/** @constructor */
function $h_sc_Hashing$() {
}
$h_sc_Hashing$.prototype = $p;
$p.c0 = (function(hcode) {
  var h = ((hcode + (~(hcode << 9))) | 0);
  h = (h ^ ((h >>> 14) | 0));
  h = ((h + (h << 4)) | 0);
  return (h ^ ((h >>> 10) | 0));
});
var $d_sc_Hashing$ = new $TypeData().i($c_sc_Hashing$, "scala.collection.Hashing$", ({
  fo: 1
}));
var $n_sc_Hashing$;
function $m_sc_Hashing$() {
  if ((!$n_sc_Hashing$)) {
    $n_sc_Hashing$ = new $c_sc_Hashing$();
  }
  return $n_sc_Hashing$;
}
function $f_sc_IterableOnceOps__foreach__F1__V($thiz, f) {
  var it = $thiz.i();
  while (it.m()) {
    f.b(it.g());
  }
}
function $f_sc_IterableOnceOps__forall__F1__Z($thiz, p) {
  var res = true;
  var it = $thiz.i();
  while ((res && it.m())) {
    res = (!(!p.b(it.g())));
  }
  return res;
}
function $f_sc_IterableOnceOps__isEmpty__Z($thiz) {
  var x30 = $thiz.x();
  if ((x30 === (-1))) {
    return (!$thiz.i().m());
  }
  if ((x30 === 0)) {
    return true;
  }
  return false;
}
function $f_sc_IterableOnceOps__size__I($thiz) {
  if (($thiz.x() >= 0)) {
    return $thiz.x();
  } else {
    var it = $thiz.i();
    var len = 0;
    while (it.m()) {
      len = ((1 + len) | 0);
      it.g();
    }
    return len;
  }
}
function $f_sc_IterableOnceOps__copyToArray__O__I__I__I($thiz, dest, start, n) {
  var it = $thiz.i();
  var i = start;
  matchResult18: {
    var srclen;
    var x31 = $thiz.x();
    if ((x31 === (-1))) {
      var srclen = $m_jl_reflect_Array$().bJ(dest);
      break matchResult18;
    }
    var srclen = x31;
  }
  var destLen = $m_jl_reflect_Array$().bJ(dest);
  var limit = ((n < srclen) ? n : srclen);
  var capacity = ((start < 0) ? destLen : ((destLen - start) | 0));
  var total = ((capacity < limit) ? capacity : limit);
  var end = ((start + ((total < 0) ? 0 : total)) | 0);
  while (((i < end) && it.m())) {
    $m_sr_ScalaRunTime$().gY(dest, i, it.g());
    i = ((1 + i) | 0);
  }
  return ((i - start) | 0);
}
function $f_sc_IterableOnceOps__mkString__T__T__T__T($thiz, start, sep, end) {
  return (($thiz.x() === 0) ? (("" + start) + end) : $thiz.dy($ct_scm_StringBuilder__(new $c_scm_StringBuilder()), start, sep, end).aM.p);
}
function $f_sc_IterableOnceOps__addString__scm_StringBuilder__T__T__T__scm_StringBuilder($thiz, b, start, sep, end) {
  var jsb = b.aM;
  if ((start.length !== 0)) {
    jsb.p = (("" + jsb.p) + start);
  }
  var it = $thiz.i();
  if (it.m()) {
    var obj = it.g();
    jsb.p = (("" + jsb.p) + obj);
    while (it.m()) {
      if ((sep.length !== 0)) {
        jsb.p = (("" + jsb.p) + sep);
      }
      var obj$1 = it.g();
      jsb.p = (("" + jsb.p) + obj$1);
    }
  }
  if ((end.length !== 0)) {
    jsb.p = (("" + jsb.p) + end);
  }
  return b;
}
function $f_sc_IterableOnceOps__toArray__s_reflect_ClassTag__O($thiz, evidence$1) {
  if (($thiz.x() >= 0)) {
    var length = $thiz.x();
    var destination = evidence$1.bo(length);
    $thiz.bI(destination, 0, 2147483647);
    return destination;
  } else {
    var capacity = 0;
    var size = 0;
    var jsElems = null;
    var elementClass = evidence$1.aC();
    capacity = 0;
    size = 0;
    var isCharArrayBuilder = (elementClass === $d_C.l());
    jsElems = [];
    var it = $thiz.i();
    while (it.m()) {
      var elem = it.g();
      var unboxedElem = (isCharArrayBuilder ? $uC(elem) : ((elem === null) ? $m_scm_ArrayBuilder$().hk(elementClass) : elem));
      jsElems.push(unboxedElem);
    }
    return $m_scm_ArrayBuilder$().hj(((elementClass === $d_V.l()) ? $d_jl_Void.l() : (((elementClass === $d_sr_Null$.l()) || (elementClass === $d_sr_Nothing$.l())) ? $d_O.l() : elementClass)), jsElems);
  }
}
/** @constructor */
function $c_sc_Iterator$ConcatIteratorCell(head, tail) {
  this.m6 = null;
  this.ft = null;
  this.m6 = head;
  this.ft = tail;
}
$p = $c_sc_Iterator$ConcatIteratorCell.prototype = new $h_O();
$p.constructor = $c_sc_Iterator$ConcatIteratorCell;
/** @constructor */
function $h_sc_Iterator$ConcatIteratorCell() {
}
$h_sc_Iterator$ConcatIteratorCell.prototype = $p;
$p.qi = (function() {
  return this.m6.F().i();
});
var $d_sc_Iterator$ConcatIteratorCell = new $TypeData().i($c_sc_Iterator$ConcatIteratorCell, "scala.collection.Iterator$ConcatIteratorCell", ({
  fx: 1
}));
/** @constructor */
function $c_sc_StringOps$() {
  this.m9 = null;
  $n_sc_StringOps$ = this;
  this.m9 = new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((_$1$2) => this.m9));
}
$p = $c_sc_StringOps$.prototype = new $h_O();
$p.constructor = $c_sc_StringOps$;
/** @constructor */
function $h_sc_StringOps$() {
}
$h_sc_StringOps$.prototype = $p;
$p.pv = (function(this$, elem) {
  return ($f_T__indexOf__I__I(this$, elem) >= 0);
});
$p.gh = (function(this$, marginChar) {
  var sb = $ct_jl_StringBuilder__I__(new $c_jl_StringBuilder(), this$.length);
  var this$1 = new $c_sc_StringOps$$anon$1(this$, false);
  while ((this$1.aD < this$1.dR)) {
    var x0 = this$1.nR();
    var len = x0.length;
    var index = 0;
    while (((index < len) && (x0.charCodeAt(index) <= 32))) {
      index = ((1 + index) | 0);
    }
    if (((index < len) && (x0.charCodeAt(index) === marginChar))) {
      var beginIndex = ((1 + index) | 0);
      var stripped = x0.substring(beginIndex);
    } else {
      var stripped = x0;
    }
    sb.p = (("" + sb.p) + stripped);
  }
  return sb.p;
});
var $d_sc_StringOps$ = new $TypeData().i($c_sc_StringOps$, "scala.collection.StringOps$", ({
  fE: 1
}));
var $n_sc_StringOps$;
function $m_sc_StringOps$() {
  if ((!$n_sc_StringOps$)) {
    $n_sc_StringOps$ = new $c_sc_StringOps$();
  }
  return $n_sc_StringOps$;
}
/** @constructor */
function $c_scg_CommonErrors$() {
}
$p = $c_scg_CommonErrors$.prototype = new $h_O();
$p.constructor = $c_scg_CommonErrors$;
/** @constructor */
function $h_scg_CommonErrors$() {
}
$h_scg_CommonErrors$.prototype = $p;
$p.ja = (function(index, max) {
  return $ct_jl_IndexOutOfBoundsException__T__(new $c_jl_IndexOutOfBoundsException(), (((index + " is out of bounds (min 0, max ") + max) + ")"));
});
var $d_scg_CommonErrors$ = new $TypeData().i($c_scg_CommonErrors$, "scala.collection.generic.CommonErrors$", ({
  fJ: 1
}));
var $n_scg_CommonErrors$;
function $m_scg_CommonErrors$() {
  if ((!$n_scg_CommonErrors$)) {
    $n_scg_CommonErrors$ = new $c_scg_CommonErrors$();
  }
  return $n_scg_CommonErrors$;
}
/** @constructor */
function $c_sci_IndexedSeqDefaults$() {
  this.mf = 0;
  $n_sci_IndexedSeqDefaults$ = this;
  try {
    $m_sc_StringOps$();
    var $x_1 = $m_jl_Integer$().nJ($m_jl_System$SystemProperties$().j7("scala.collection.immutable.IndexedSeq.defaultApplyPreferredMaxLength", "64"), 10, 214748364);
  } catch (e) {
    if (false) {
      var $x_1 = 64;
    } else {
      var $x_1;
      throw e;
    }
  }
  this.mf = $x_1;
}
$p = $c_sci_IndexedSeqDefaults$.prototype = new $h_O();
$p.constructor = $c_sci_IndexedSeqDefaults$;
/** @constructor */
function $h_sci_IndexedSeqDefaults$() {
}
$h_sci_IndexedSeqDefaults$.prototype = $p;
var $d_sci_IndexedSeqDefaults$ = new $TypeData().i($c_sci_IndexedSeqDefaults$, "scala.collection.immutable.IndexedSeqDefaults$", ({
  fR: 1
}));
var $n_sci_IndexedSeqDefaults$;
function $m_sci_IndexedSeqDefaults$() {
  if ((!$n_sci_IndexedSeqDefaults$)) {
    $n_sci_IndexedSeqDefaults$ = new $c_sci_IndexedSeqDefaults$();
  }
  return $n_sci_IndexedSeqDefaults$;
}
/** @constructor */
function $c_sci_LazyList$EmptyMarker$() {
}
$p = $c_sci_LazyList$EmptyMarker$.prototype = new $h_O();
$p.constructor = $c_sci_LazyList$EmptyMarker$;
/** @constructor */
function $h_sci_LazyList$EmptyMarker$() {
}
$h_sci_LazyList$EmptyMarker$.prototype = $p;
var $d_sci_LazyList$EmptyMarker$ = new $TypeData().i($c_sci_LazyList$EmptyMarker$, "scala.collection.immutable.LazyList$EmptyMarker$", ({
  fU: 1
}));
var $n_sci_LazyList$EmptyMarker$;
function $m_sci_LazyList$EmptyMarker$() {
  if ((!$n_sci_LazyList$EmptyMarker$)) {
    $n_sci_LazyList$EmptyMarker$ = new $c_sci_LazyList$EmptyMarker$();
  }
  return $n_sci_LazyList$EmptyMarker$;
}
/** @constructor */
function $c_sci_LazyList$LazyBuilder$DeferredState() {
  this.ik = null;
}
$p = $c_sci_LazyList$LazyBuilder$DeferredState.prototype = new $h_O();
$p.constructor = $c_sci_LazyList$LazyBuilder$DeferredState;
/** @constructor */
function $h_sci_LazyList$LazyBuilder$DeferredState() {
}
$h_sci_LazyList$LazyBuilder$DeferredState.prototype = $p;
$p.iV = (function() {
  var state = this.ik;
  if ((state === null)) {
    throw new $c_jl_IllegalStateException("uninitialized");
  }
  return state.F();
});
$p.jb = (function(state) {
  if ((this.ik !== null)) {
    throw new $c_jl_IllegalStateException("already initialized");
  }
  this.ik = state;
});
var $d_sci_LazyList$LazyBuilder$DeferredState = new $TypeData().i($c_sci_LazyList$LazyBuilder$DeferredState, "scala.collection.immutable.LazyList$LazyBuilder$DeferredState", ({
  fW: 1
}));
/** @constructor */
function $c_sci_LazyList$MidEvaluation$() {
}
$p = $c_sci_LazyList$MidEvaluation$.prototype = new $h_O();
$p.constructor = $c_sci_LazyList$MidEvaluation$;
/** @constructor */
function $h_sci_LazyList$MidEvaluation$() {
}
$h_sci_LazyList$MidEvaluation$.prototype = $p;
var $d_sci_LazyList$MidEvaluation$ = new $TypeData().i($c_sci_LazyList$MidEvaluation$, "scala.collection.immutable.LazyList$MidEvaluation$", ({
  fY: 1
}));
var $n_sci_LazyList$MidEvaluation$;
function $m_sci_LazyList$MidEvaluation$() {
  if ((!$n_sci_LazyList$MidEvaluation$)) {
    $n_sci_LazyList$MidEvaluation$ = new $c_sci_LazyList$MidEvaluation$();
  }
  return $n_sci_LazyList$MidEvaluation$;
}
/** @constructor */
function $c_sci_MapNode$() {
  this.mi = null;
  $n_sci_MapNode$ = this;
  $m_s_reflect_ManifestFactory$IntManifest$();
  this.mi = new $c_sci_BitmapIndexedMapNode(0, 0, new $ac_O(0), new $ac_I(0), 0, 0);
}
$p = $c_sci_MapNode$.prototype = new $h_O();
$p.constructor = $c_sci_MapNode$;
/** @constructor */
function $h_sci_MapNode$() {
}
$h_sci_MapNode$.prototype = $p;
var $d_sci_MapNode$ = new $TypeData().i($c_sci_MapNode$, "scala.collection.immutable.MapNode$", ({
  ge: 1
}));
var $n_sci_MapNode$;
function $m_sci_MapNode$() {
  if ((!$n_sci_MapNode$)) {
    $n_sci_MapNode$ = new $c_sci_MapNode$();
  }
  return $n_sci_MapNode$;
}
function $p_sci_Node__arrayIndexOutOfBounds__O__I__jl_ArrayIndexOutOfBoundsException($thiz, as, ix) {
  return $ct_jl_ArrayIndexOutOfBoundsException__T__(new $c_jl_ArrayIndexOutOfBoundsException(), ((ix + " is out of bounds (min 0, max ") + (($m_jl_reflect_Array$().bJ(as) - 1) | 0)));
}
/** @constructor */
function $c_sci_Node() {
}
$p = $c_sci_Node.prototype = new $h_O();
$p.constructor = $c_sci_Node;
/** @constructor */
function $h_sci_Node() {
}
$h_sci_Node.prototype = $p;
$p.o2 = (function(as, ix) {
  if ((ix < 0)) {
    throw $p_sci_Node__arrayIndexOutOfBounds__O__I__jl_ArrayIndexOutOfBoundsException(this, as, ix);
  }
  if ((ix > ((as.a.length - 1) | 0))) {
    throw $p_sci_Node__arrayIndexOutOfBounds__O__I__jl_ArrayIndexOutOfBoundsException(this, as, ix);
  }
  var result = new $ac_I(((as.a.length - 1) | 0));
  as.u(0, result, 0, ix);
  var srcPos = ((1 + ix) | 0);
  var length = ((((as.a.length - ix) | 0) - 1) | 0);
  as.u(srcPos, result, ix, length);
  return result;
});
$p.qq = (function(as, ix, elem) {
  if ((ix < 0)) {
    throw $p_sci_Node__arrayIndexOutOfBounds__O__I__jl_ArrayIndexOutOfBoundsException(this, as, ix);
  }
  if ((ix > as.a.length)) {
    throw $p_sci_Node__arrayIndexOutOfBounds__O__I__jl_ArrayIndexOutOfBoundsException(this, as, ix);
  }
  var result = new $ac_I(((1 + as.a.length) | 0));
  as.u(0, result, 0, ix);
  result.a[ix] = elem;
  var destPos = ((1 + ix) | 0);
  var length = ((as.a.length - ix) | 0);
  as.u(ix, result, destPos, length);
  return result;
});
var $d_sci_Node = new $TypeData().i(0, "scala.collection.immutable.Node", ({
  aR: 1
}));
/** @constructor */
function $c_sci_Node$() {
  this.fC = 0;
  $n_sci_Node$ = this;
  this.fC = $doubleToInt((+Math.ceil(6.4)));
}
$p = $c_sci_Node$.prototype = new $h_O();
$p.constructor = $c_sci_Node$;
/** @constructor */
function $h_sci_Node$() {
}
$h_sci_Node$.prototype = $p;
$p.dE = (function(hash, shift) {
  return (31 & ((hash >>> shift) | 0));
});
$p.cU = (function(mask) {
  return (1 << mask);
});
$p.qk = (function(bitmap, bitpos) {
  return $m_jl_Integer$().dA((bitmap & ((bitpos - 1) | 0)));
});
$p.c1 = (function(bitmap, mask, bitpos) {
  return ((bitmap === (-1)) ? mask : this.qk(bitmap, bitpos));
});
var $d_sci_Node$ = new $TypeData().i($c_sci_Node$, "scala.collection.immutable.Node$", ({
  gh: 1
}));
var $n_sci_Node$;
function $m_sci_Node$() {
  if ((!$n_sci_Node$)) {
    $n_sci_Node$ = new $c_sci_Node$();
  }
  return $n_sci_Node$;
}
/** @constructor */
function $c_sci_VectorStatics$() {
  this.ip = null;
  this.bk = null;
  this.cm = null;
  this.eC = null;
  this.iq = null;
  this.mm = null;
  $n_sci_VectorStatics$ = this;
  this.ip = new $ac_O(0);
  this.bk = new ($d_O.r().r().C)(0);
  this.cm = new ($d_O.r().r().r().C)(0);
  this.eC = new ($d_O.r().r().r().r().C)(0);
  this.iq = new ($d_O.r().r().r().r().r().C)(0);
  this.mm = new ($d_O.r().r().r().r().r().r().C)(0);
}
$p = $c_sci_VectorStatics$.prototype = new $h_O();
$p.constructor = $c_sci_VectorStatics$;
/** @constructor */
function $h_sci_VectorStatics$() {
}
$h_sci_VectorStatics$.prototype = $p;
$p.eO = (function(a, elem) {
  var alen = a.a.length;
  var ac = new $ac_O(((1 + alen) | 0));
  a.u(0, ac, 0, alen);
  ac.a[alen] = elem;
  return ac;
});
$p.z = (function(a, elem) {
  var ac = $m_ju_Arrays$().S(a, ((1 + a.a.length) | 0));
  ac.a[((ac.a.length - 1) | 0)] = elem;
  return ac;
});
$p.cp = (function(elem, a) {
  var ac = $objectGetClass(a).ah.Q().ah.U(((1 + a.a.length) | 0));
  var length$1 = a.a.length;
  a.u(0, ac, 1, length$1);
  ac.a[0] = elem;
  return ac;
});
$p.iZ = (function(level, a, f) {
  var i = 0;
  var len = a.a.length;
  if ((level === 0)) {
    while ((i < len)) {
      f.b(a.a[i]);
      i = ((1 + i) | 0);
    }
  } else {
    var l = ((level - 1) | 0);
    while ((i < len)) {
      this.iZ(l, a.a[i], f);
      i = ((1 + i) | 0);
    }
  }
});
var $d_sci_VectorStatics$ = new $TypeData().i($c_sci_VectorStatics$, "scala.collection.immutable.VectorStatics$", ({
  gy: 1
}));
var $n_sci_VectorStatics$;
function $m_sci_VectorStatics$() {
  if ((!$n_sci_VectorStatics$)) {
    $n_sci_VectorStatics$ = new $c_sci_VectorStatics$();
  }
  return $n_sci_VectorStatics$;
}
/** @constructor */
function $c_scm_ArrayBuilder$() {
}
$p = $c_scm_ArrayBuilder$.prototype = new $h_O();
$p.constructor = $c_scm_ArrayBuilder$;
/** @constructor */
function $h_scm_ArrayBuilder$() {
}
$h_scm_ArrayBuilder$.prototype = $p;
$p.hk = (function(runtimeClass) {
  return ((runtimeClass === $d_B.l()) ? 0 : ((runtimeClass === $d_S.l()) ? 0 : ((runtimeClass === $d_C.l()) ? 0 : ((runtimeClass === $d_I.l()) ? 0 : ((runtimeClass === $d_J.l()) ? $bL(0, 0) : ((runtimeClass === $d_F.l()) ? 0.0 : ((runtimeClass === $d_D.l()) ? 0.0 : ((runtimeClass === $d_Z.l()) ? false : ((runtimeClass === $d_V.l()) ? (void 0) : null)))))))));
});
$p.hj = (function(runtimeClass, a) {
  var len = (a.length | 0);
  if ((runtimeClass === $d_C.l())) {
    var result = new $ac_C(len);
    var i = 0;
    while ((i !== len)) {
      result.a[i] = (65535 & (a[i] | 0));
      i = ((1 + i) | 0);
    }
    return result;
  } else {
    var result$2 = runtimeClass.ah.U(len);
    var i$2 = 0;
    while ((i$2 !== len)) {
      $m_sr_ScalaRunTime$().gY(result$2, i$2, a[i$2]);
      i$2 = ((1 + i$2) | 0);
    }
    return result$2;
  }
});
var $d_scm_ArrayBuilder$ = new $TypeData().i($c_scm_ArrayBuilder$, "scala.collection.mutable.ArrayBuilder$", ({
  gF: 1
}));
var $n_scm_ArrayBuilder$;
function $m_scm_ArrayBuilder$() {
  if ((!$n_scm_ArrayBuilder$)) {
    $n_scm_ArrayBuilder$ = new $c_scm_ArrayBuilder$();
  }
  return $n_scm_ArrayBuilder$;
}
/** @constructor */
function $c_scm_HashSet$Node(_key, _hash, _next) {
  this.eF = null;
  this.cQ = 0;
  this.aL = null;
  this.eF = _key;
  this.cQ = _hash;
  this.aL = _next;
}
$p = $c_scm_HashSet$Node.prototype = new $h_O();
$p.constructor = $c_scm_HashSet$Node;
/** @constructor */
function $h_scm_HashSet$Node() {
}
$h_scm_HashSet$Node.prototype = $p;
$p.pX = (function(k, h) {
  var \u03b4this$tailLocal1 = this;
  while (true) {
    if (((h === \u03b4this$tailLocal1.cQ) && $m_sr_BoxesRunTime$().j(k, \u03b4this$tailLocal1.eF))) {
      return \u03b4this$tailLocal1;
    } else if (((\u03b4this$tailLocal1.aL === null) || (\u03b4this$tailLocal1.cQ > h))) {
      return null;
    } else {
      \u03b4this$tailLocal1 = \u03b4this$tailLocal1.aL;
    }
  }
});
$p.t = (function() {
  return ((((("Node(" + this.eF) + ", ") + this.cQ) + ") -> ") + this.aL);
});
var $d_scm_HashSet$Node = new $TypeData().i($c_scm_HashSet$Node, "scala.collection.mutable.HashSet$Node", ({
  gR: 1
}));
/** @constructor */
function $c_scm_MutationTracker$() {
}
$p = $c_scm_MutationTracker$.prototype = new $h_O();
$p.constructor = $c_scm_MutationTracker$;
/** @constructor */
function $h_scm_MutationTracker$() {
}
$h_scm_MutationTracker$.prototype = $p;
$p.nd = (function(expectedCount, actualCount, message) {
  if ((actualCount !== expectedCount)) {
    throw new $c_ju_ConcurrentModificationException(message);
  }
});
var $d_scm_MutationTracker$ = new $TypeData().i($c_scm_MutationTracker$, "scala.collection.mutable.MutationTracker$", ({
  gX: 1
}));
var $n_scm_MutationTracker$;
function $m_scm_MutationTracker$() {
  if ((!$n_scm_MutationTracker$)) {
    $n_scm_MutationTracker$ = new $c_scm_MutationTracker$();
  }
  return $n_scm_MutationTracker$;
}
function $ct_s_concurrent_BatchingExecutor$AbstractBatch__jl_Runnable__Ajl_Runnable__I__($thiz, first, other, size) {
  $thiz.fH = first;
  $thiz.fI = other;
  $thiz.dv = size;
  return $thiz;
}
function $p_s_concurrent_BatchingExecutor$AbstractBatch__ensureCapacity__I__Ajl_Runnable($thiz, curSize) {
  var curOther = $thiz.fI;
  var curLen = curOther.a.length;
  if ((curSize <= curLen)) {
    return curOther;
  } else {
    var newLen = ((curLen === 0) ? 4 : (curLen << 1));
    if ((newLen <= curLen)) {
      throw new $c_jl_StackOverflowError(("Space limit of asynchronous stack reached: " + curLen));
    }
    var newOther = new ($d_jl_Runnable.r().C)(newLen);
    curOther.u(0, newOther, 0, curLen);
    $thiz.fI = newOther;
    return newOther;
  }
}
/** @constructor */
function $c_s_concurrent_BatchingExecutor$AbstractBatch() {
  this.fH = null;
  this.fI = null;
  this.dv = 0;
}
$p = $c_s_concurrent_BatchingExecutor$AbstractBatch.prototype = new $h_O();
$p.constructor = $c_s_concurrent_BatchingExecutor$AbstractBatch;
/** @constructor */
function $h_s_concurrent_BatchingExecutor$AbstractBatch() {
}
$h_s_concurrent_BatchingExecutor$AbstractBatch.prototype = $p;
$p.qQ = (function(r) {
  var sz = this.dv;
  if ((sz === 0)) {
    this.fH = r;
  } else {
    $p_s_concurrent_BatchingExecutor$AbstractBatch__ensureCapacity__I__Ajl_Runnable(this, sz).a[((sz - 1) | 0)] = r;
  }
  this.dv = ((1 + sz) | 0);
});
$p.r7 = (function(n) {
  var n$tailLocal1 = n;
  while (true) {
    if ((n$tailLocal1 > 0)) {
      var x1 = this.dv;
      if ((x1 === 0)) {
        return (void 0);
      }
      if ((x1 === 1)) {
        var x$proxy1 = this.fH;
        if ((x$proxy1 === null)) {
          $m_sr_Scala3RunTime$().bp();
        }
        this.fH = null;
        this.dv = 0;
        x$proxy1.e8();
        n$tailLocal1 = ((n$tailLocal1 - 1) | 0);
        continue;
      }
      var o = this.fI;
      var x$proxy2 = o.a[((x1 - 2) | 0)];
      if ((x$proxy2 === null)) {
        $m_sr_Scala3RunTime$().bp();
      }
      o.a[((x1 - 2) | 0)] = null;
      this.dv = ((x1 - 1) | 0);
      x$proxy2.e8();
      n$tailLocal1 = ((n$tailLocal1 - 1) | 0);
    } else {
      return (void 0);
    }
  }
});
/** @constructor */
function $c_s_concurrent_BatchingExecutorStatics$() {
  this.my = null;
  $n_s_concurrent_BatchingExecutorStatics$ = this;
  this.my = new ($d_jl_Runnable.r().C)(0);
}
$p = $c_s_concurrent_BatchingExecutorStatics$.prototype = new $h_O();
$p.constructor = $c_s_concurrent_BatchingExecutorStatics$;
/** @constructor */
function $h_s_concurrent_BatchingExecutorStatics$() {
}
$h_s_concurrent_BatchingExecutorStatics$.prototype = $p;
var $d_s_concurrent_BatchingExecutorStatics$ = new $TypeData().i($c_s_concurrent_BatchingExecutorStatics$, "scala.concurrent.BatchingExecutorStatics$", ({
  h4: 1
}));
var $n_s_concurrent_BatchingExecutorStatics$;
function $m_s_concurrent_BatchingExecutorStatics$() {
  if ((!$n_s_concurrent_BatchingExecutorStatics$)) {
    $n_s_concurrent_BatchingExecutorStatics$ = new $c_s_concurrent_BatchingExecutorStatics$();
  }
  return $n_s_concurrent_BatchingExecutorStatics$;
}
/** @constructor */
function $c_s_concurrent_ExecutionContext$() {
  this.mz = null;
  this.mA = false;
  this.eG = null;
  $n_s_concurrent_ExecutionContext$ = this;
  this.eG = new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((_$1$3) => {
    _$1$3.gc($m_jl_System$Streams$().ev);
  }));
}
$p = $c_s_concurrent_ExecutionContext$.prototype = new $h_O();
$p.constructor = $c_s_concurrent_ExecutionContext$;
/** @constructor */
function $h_s_concurrent_ExecutionContext$() {
}
$h_s_concurrent_ExecutionContext$.prototype = $p;
$p.g4 = (function() {
  if ((!this.mA)) {
    this.mz = $m_sjs_concurrent_JSExecutionContext$().mL;
    this.mA = true;
  }
  return this.mz;
});
var $d_s_concurrent_ExecutionContext$ = new $TypeData().i($c_s_concurrent_ExecutionContext$, "scala.concurrent.ExecutionContext$", ({
  h5: 1
}));
var $n_s_concurrent_ExecutionContext$;
function $m_s_concurrent_ExecutionContext$() {
  if ((!$n_s_concurrent_ExecutionContext$)) {
    $n_s_concurrent_ExecutionContext$ = new $c_s_concurrent_ExecutionContext$();
  }
  return $n_s_concurrent_ExecutionContext$;
}
/** @constructor */
function $c_s_concurrent_Future$() {
  this.mC = null;
  this.mE = null;
  this.mD = null;
  this.iz = null;
  this.mF = null;
  $n_s_concurrent_Future$ = this;
  $m_sci_Map$().nx(new $c_sjsr_WrappedVarArgs([new $c_T2($d_Z.l(), $d_jl_Boolean.l()), new $c_T2($d_B.l(), $d_jl_Byte.l()), new $c_T2($d_C.l(), $d_jl_Character.l()), new $c_T2($d_S.l(), $d_jl_Short.l()), new $c_T2($d_I.l(), $d_jl_Integer.l()), new $c_T2($d_J.l(), $d_jl_Long.l()), new $c_T2($d_F.l(), $d_jl_Float.l()), new $c_T2($d_D.l(), $d_jl_Double.l()), new $c_T2($d_V.l(), $d_jl_Void.l())]));
  this.mC = new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((t$2) => {
    throw new $c_s_concurrent_Future$$anon$1(t$2);
  }));
  this.mE = new $c_s_util_Failure(new $c_s_concurrent_Future$$anon$2());
  this.mD = new $c_s_util_Failure(new $c_s_concurrent_Future$$anon$3());
  $m_s_concurrent_Future$().nC(this.mD);
  this.iz = $m_s_concurrent_Future$().pV(new $c_s_concurrent_Future$$anon$4());
  this.mF = new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((t$2$1) => this.iz));
  this.nC(new $c_s_util_Success((void 0)));
}
$p = $c_s_concurrent_Future$.prototype = new $h_O();
$p.constructor = $c_s_concurrent_Future$;
/** @constructor */
function $h_s_concurrent_Future$() {
}
$h_s_concurrent_Future$.prototype = $p;
$p.pV = (function(exception) {
  return $m_s_concurrent_Promise$().pW(exception);
});
$p.rj = (function(result) {
  return $m_s_concurrent_Promise$().rk(result);
});
$p.nC = (function(result) {
  return $ct_s_concurrent_impl_Promise$DefaultPromise__s_util_Try__(new $c_s_concurrent_impl_Promise$DefaultPromise(), result);
});
var $d_s_concurrent_Future$ = new $TypeData().i($c_s_concurrent_Future$, "scala.concurrent.Future$", ({
  h7: 1
}));
var $n_s_concurrent_Future$;
function $m_s_concurrent_Future$() {
  if ((!$n_s_concurrent_Future$)) {
    $n_s_concurrent_Future$ = new $c_s_concurrent_Future$();
  }
  return $n_s_concurrent_Future$;
}
function $f_s_concurrent_Promise__complete__s_util_Try__s_concurrent_Promise($thiz, result) {
  if ($thiz.rB(result)) {
    return $thiz;
  } else {
    throw new $c_jl_IllegalStateException("Promise already completed.");
  }
}
function $f_s_concurrent_Promise__success__O__s_concurrent_Promise($thiz, value) {
  return $f_s_concurrent_Promise__complete__s_util_Try__s_concurrent_Promise($thiz, new $c_s_util_Success(value));
}
function $f_s_concurrent_Promise__failure__jl_Throwable__s_concurrent_Promise($thiz, cause) {
  return $f_s_concurrent_Promise__complete__s_util_Try__s_concurrent_Promise($thiz, new $c_s_util_Failure(cause));
}
/** @constructor */
function $c_s_concurrent_Promise$() {
}
$p = $c_s_concurrent_Promise$.prototype = new $h_O();
$p.constructor = $c_s_concurrent_Promise$;
/** @constructor */
function $h_s_concurrent_Promise$() {
}
$h_s_concurrent_Promise$.prototype = $p;
$p.pW = (function(exception) {
  return $ct_s_concurrent_impl_Promise$DefaultPromise__s_util_Try__(new $c_s_concurrent_impl_Promise$DefaultPromise(), new $c_s_util_Failure(exception));
});
$p.rk = (function(result) {
  return $ct_s_concurrent_impl_Promise$DefaultPromise__s_util_Try__(new $c_s_concurrent_impl_Promise$DefaultPromise(), new $c_s_util_Success(result));
});
var $d_s_concurrent_Promise$ = new $TypeData().i($c_s_concurrent_Promise$, "scala.concurrent.Promise$", ({
  hc: 1
}));
var $n_s_concurrent_Promise$;
function $m_s_concurrent_Promise$() {
  if ((!$n_s_concurrent_Promise$)) {
    $n_s_concurrent_Promise$ = new $c_s_concurrent_Promise$();
  }
  return $n_s_concurrent_Promise$;
}
/** @constructor */
function $c_s_concurrent_impl_Promise$() {
  this.fJ = null;
  $n_s_concurrent_impl_Promise$ = this;
  this.fJ = $ct_s_concurrent_impl_Promise$Transformation__I__F1__s_concurrent_ExecutionContext__(new $c_s_concurrent_impl_Promise$Transformation(), 0, null, $m_s_concurrent_ExecutionContext$parasitic$());
}
$p = $c_s_concurrent_impl_Promise$.prototype = new $h_O();
$p.constructor = $c_s_concurrent_impl_Promise$;
/** @constructor */
function $h_s_concurrent_impl_Promise$() {
}
$h_s_concurrent_impl_Promise$.prototype = $p;
$p.gd = (function(value) {
  if ((value instanceof $c_s_util_Success)) {
    return value;
  } else {
    var t = value.c7;
    return (((false || false) || (t instanceof $c_jl_Error)) ? (false ? new $c_s_util_Success(t.op()) : new $c_s_util_Failure(new $c_ju_concurrent_ExecutionException("Boxed Exception", t))) : value);
  }
});
var $d_s_concurrent_impl_Promise$ = new $TypeData().i($c_s_concurrent_impl_Promise$, "scala.concurrent.impl.Promise$", ({
  hd: 1
}));
var $n_s_concurrent_impl_Promise$;
function $m_s_concurrent_impl_Promise$() {
  if ((!$n_s_concurrent_impl_Promise$)) {
    $n_s_concurrent_impl_Promise$ = new $c_s_concurrent_impl_Promise$();
  }
  return $n_s_concurrent_impl_Promise$;
}
function $is_s_concurrent_impl_Promise$Callbacks(obj) {
  return (!(!((obj && obj.$classData) && obj.$classData.n.av)));
}
function $isArrayOf_s_concurrent_impl_Promise$Callbacks(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.av)));
}
/** @constructor */
function $c_s_reflect_ClassTag$() {
  this.oF = null;
  this.oO = null;
  this.oG = null;
  this.oJ = null;
  this.oK = null;
  this.oI = null;
  this.oH = null;
  this.oE = null;
  this.oP = null;
  this.oD = null;
  this.oN = null;
  this.oL = null;
  this.oM = null;
  $n_s_reflect_ClassTag$ = this;
  this.oF = $m_s_reflect_ManifestFactory$ByteManifest$();
  this.oO = $m_s_reflect_ManifestFactory$ShortManifest$();
  this.oG = $m_s_reflect_ManifestFactory$CharManifest$();
  this.oJ = $m_s_reflect_ManifestFactory$IntManifest$();
  this.oK = $m_s_reflect_ManifestFactory$LongManifest$();
  this.oI = $m_s_reflect_ManifestFactory$FloatManifest$();
  this.oH = $m_s_reflect_ManifestFactory$DoubleManifest$();
  this.oE = $m_s_reflect_ManifestFactory$BooleanManifest$();
  this.oP = $m_s_reflect_ManifestFactory$UnitManifest$();
  this.oD = $m_s_reflect_ManifestFactory$AnyManifest$();
  this.oN = $m_s_reflect_ManifestFactory$ObjectManifest$();
  this.oL = $m_s_reflect_ManifestFactory$NothingManifest$();
  this.oM = $m_s_reflect_ManifestFactory$NullManifest$();
}
$p = $c_s_reflect_ClassTag$.prototype = new $h_O();
$p.constructor = $c_s_reflect_ClassTag$;
/** @constructor */
function $h_s_reflect_ClassTag$() {
}
$h_s_reflect_ClassTag$.prototype = $p;
$p.n8 = (function(runtimeClass1) {
  return ((runtimeClass1 === $d_B.l()) ? $m_s_reflect_ManifestFactory$ByteManifest$() : ((runtimeClass1 === $d_S.l()) ? $m_s_reflect_ManifestFactory$ShortManifest$() : ((runtimeClass1 === $d_C.l()) ? $m_s_reflect_ManifestFactory$CharManifest$() : ((runtimeClass1 === $d_I.l()) ? $m_s_reflect_ManifestFactory$IntManifest$() : ((runtimeClass1 === $d_J.l()) ? $m_s_reflect_ManifestFactory$LongManifest$() : ((runtimeClass1 === $d_F.l()) ? $m_s_reflect_ManifestFactory$FloatManifest$() : ((runtimeClass1 === $d_D.l()) ? $m_s_reflect_ManifestFactory$DoubleManifest$() : ((runtimeClass1 === $d_Z.l()) ? $m_s_reflect_ManifestFactory$BooleanManifest$() : ((runtimeClass1 === $d_V.l()) ? $m_s_reflect_ManifestFactory$UnitManifest$() : ((runtimeClass1 === $d_O.l()) ? $m_s_reflect_ManifestFactory$ObjectManifest$() : ((runtimeClass1 === $d_sr_Nothing$.l()) ? $m_s_reflect_ManifestFactory$NothingManifest$() : ((runtimeClass1 === $d_sr_Null$.l()) ? $m_s_reflect_ManifestFactory$NullManifest$() : new $c_s_reflect_ClassTag$GenericClassTag(runtimeClass1)))))))))))));
});
var $d_s_reflect_ClassTag$ = new $TypeData().i($c_s_reflect_ClassTag$, "scala.reflect.ClassTag$", ({
  hh: 1
}));
var $n_s_reflect_ClassTag$;
function $m_s_reflect_ClassTag$() {
  if ((!$n_s_reflect_ClassTag$)) {
    $n_s_reflect_ClassTag$ = new $c_s_reflect_ClassTag$();
  }
  return $n_s_reflect_ClassTag$;
}
/** @constructor */
function $c_sr_BoxesRunTime$() {
}
$p = $c_sr_BoxesRunTime$.prototype = new $h_O();
$p.constructor = $c_sr_BoxesRunTime$;
/** @constructor */
function $h_sr_BoxesRunTime$() {
}
$h_sr_BoxesRunTime$.prototype = $p;
$p.j = (function(x, y) {
  return ((x === y) || ($is_jl_Number(x) ? this.pT(x, y) : ((x instanceof $Char) ? this.pR(x, y) : ((x === null) ? (y === null) : $dp_equals__O__Z(x, y)))));
});
$p.pT = (function(xn, y) {
  if ($is_jl_Number(y)) {
    return this.pS(xn, y);
  } else if ((y instanceof $Char)) {
    if (((typeof xn) === "number")) {
      return ((+xn) === y.c);
    } else if ((xn instanceof $Long)) {
      var $x_1 = $uJ(xn);
      var x3_$_lo = $x_1.l;
      var x3_$_hi = $x_1.h;
      var value = y.c;
      var hi = (value >> 31);
      return (((x3_$_lo ^ value) | (x3_$_hi ^ hi)) === 0);
    } else {
      return ((xn === null) ? (y === null) : $dp_equals__O__Z(xn, y));
    }
  } else {
    return ((xn === null) ? (y === null) : $dp_equals__O__Z(xn, y));
  }
});
$p.pS = (function(xn, yn) {
  if (((typeof xn) === "number")) {
    var x2 = (+xn);
    if (((typeof yn) === "number")) {
      return (x2 === (+yn));
    } else if ((yn instanceof $Long)) {
      var $x_1 = $uJ(yn);
      var x3_$_lo = $x_1.l;
      var x3_$_hi = $x_1.h;
      return (x2 === ((4.294967296E9 * x3_$_hi) + (x3_$_lo >>> 0.0)));
    } else {
      return (false && yn.k(x2));
    }
  } else if ((xn instanceof $Long)) {
    var $x_2 = $uJ(xn);
    var x3$2_$_lo = $x_2.l;
    var x3$2_$_hi = $x_2.h;
    if ((yn instanceof $Long)) {
      var $x_3 = $uJ(yn);
      var x2$3_$_lo = $x_3.l;
      var x2$3_$_hi = $x_3.h;
      return (((x3$2_$_lo ^ x2$3_$_lo) | (x3$2_$_hi ^ x2$3_$_hi)) === 0);
    } else if (((typeof yn) === "number")) {
      var x3$3 = (+yn);
      return (((4.294967296E9 * x3$2_$_hi) + (x3$2_$_lo >>> 0.0)) === x3$3);
    } else {
      return (false && yn.k($bL(x3$2_$_lo, x3$2_$_hi)));
    }
  } else {
    return ((xn === null) ? (yn === null) : $dp_equals__O__Z(xn, yn));
  }
});
$p.pR = (function(xc, y) {
  if ((y instanceof $Char)) {
    return (xc.c === y.c);
  } else if ($is_jl_Number(y)) {
    if (((typeof y) === "number")) {
      return ((+y) === xc.c);
    } else if ((y instanceof $Long)) {
      var $x_1 = $uJ(y);
      var x3_$_lo = $x_1.l;
      var x3_$_hi = $x_1.h;
      var value = xc.c;
      var hi = (value >> 31);
      return (((x3_$_lo ^ value) | (x3_$_hi ^ hi)) === 0);
    } else {
      return ((y === null) ? (xc === null) : $dp_equals__O__Z(y, xc));
    }
  } else {
    return ((xc === null) && (y === null));
  }
});
var $d_sr_BoxesRunTime$ = new $TypeData().i($c_sr_BoxesRunTime$, "scala.runtime.BoxesRunTime$", ({
  hL: 1
}));
var $n_sr_BoxesRunTime$;
function $m_sr_BoxesRunTime$() {
  if ((!$n_sr_BoxesRunTime$)) {
    $n_sr_BoxesRunTime$ = new $c_sr_BoxesRunTime$();
  }
  return $n_sr_BoxesRunTime$;
}
var $d_sr_Null$ = new $TypeData().i(0, "scala.runtime.Null$", ({
  hP: 1
}));
/** @constructor */
function $c_sr_Scala3RunTime$() {
}
$p = $c_sr_Scala3RunTime$.prototype = new $h_O();
$p.constructor = $c_sr_Scala3RunTime$;
/** @constructor */
function $h_sr_Scala3RunTime$() {
}
$h_sr_Scala3RunTime$.prototype = $p;
$p.bp = (function() {
  throw $ct_jl_NullPointerException__T__(new $c_jl_NullPointerException(), "tried to cast away nullability, but value is null");
});
var $d_sr_Scala3RunTime$ = new $TypeData().i($c_sr_Scala3RunTime$, "scala.runtime.Scala3RunTime$", ({
  hR: 1
}));
var $n_sr_Scala3RunTime$;
function $m_sr_Scala3RunTime$() {
  if ((!$n_sr_Scala3RunTime$)) {
    $n_sr_Scala3RunTime$ = new $c_sr_Scala3RunTime$();
  }
  return $n_sr_Scala3RunTime$;
}
/** @constructor */
function $c_sr_ScalaRunTime$() {
}
$p = $c_sr_ScalaRunTime$.prototype = new $h_O();
$p.constructor = $c_sr_ScalaRunTime$;
/** @constructor */
function $h_sr_ScalaRunTime$() {
}
$h_sr_ScalaRunTime$.prototype = $p;
$p.dZ = (function(xs, idx) {
  if ((xs instanceof $ac_O)) {
    return xs.a[idx];
  }
  if ((xs instanceof $ac_I)) {
    return xs.a[idx];
  }
  if ((xs instanceof $ac_D)) {
    return xs.a[idx];
  }
  if ((xs instanceof $ac_J)) {
    var $x_1 = xs.a;
    var $x_2 = (idx << 1);
    return $bL($x_1[$x_2], $x_1[(($x_2 + 1) | 0)]);
  }
  if ((xs instanceof $ac_F)) {
    return xs.a[idx];
  }
  if ((xs instanceof $ac_C)) {
    return $bC(xs.a[idx]);
  }
  if ((xs instanceof $ac_B)) {
    return xs.a[idx];
  }
  if ((xs instanceof $ac_S)) {
    return xs.a[idx];
  }
  if ((xs instanceof $ac_Z)) {
    return xs.a[idx];
  }
  if ((xs === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
  throw new $c_s_MatchError(xs);
});
$p.gY = (function(xs, idx, value) {
  if ((xs instanceof $ac_O)) {
    xs.a[idx] = value;
    return (void 0);
  }
  if ((xs instanceof $ac_I)) {
    xs.a[idx] = (value | 0);
    return (void 0);
  }
  if ((xs instanceof $ac_D)) {
    xs.a[idx] = (+value);
    return (void 0);
  }
  if ((xs instanceof $ac_J)) {
    var $x_1 = $uJ(value);
    var $x_2 = xs.a;
    var $x_3 = (idx << 1);
    $x_2[$x_3] = $x_1.l;
    $x_2[(($x_3 + 1) | 0)] = $x_1.h;
    return (void 0);
  }
  if ((xs instanceof $ac_F)) {
    xs.a[idx] = Math.fround(value);
    return (void 0);
  }
  if ((xs instanceof $ac_C)) {
    xs.a[idx] = $uC(value);
    return (void 0);
  }
  if ((xs instanceof $ac_B)) {
    xs.a[idx] = (value | 0);
    return (void 0);
  }
  if ((xs instanceof $ac_S)) {
    xs.a[idx] = (value | 0);
    return (void 0);
  }
  if ((xs instanceof $ac_Z)) {
    xs.a[idx] = (!(!value));
    return (void 0);
  }
  if ((xs === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
  throw new $c_s_MatchError(xs);
});
$p.eK = (function(x) {
  return $f_sc_IterableOnceOps__mkString__T__T__T__T(x.bx(), (x.aP() + "("), ",", ")");
});
$p.b4 = (function(xs) {
  if ((xs === null)) {
    return null;
  } else if ((xs.a.length === 0)) {
    var this$2 = $m_sci_ArraySeq$();
    $m_s_reflect_ManifestFactory$ObjectManifest$();
    return $p_sci_ArraySeq$__emptyImpl__sci_ArraySeq$ofRef(this$2);
  } else {
    return new $c_sci_ArraySeq$ofRef(xs);
  }
});
var $d_sr_ScalaRunTime$ = new $TypeData().i($c_sr_ScalaRunTime$, "scala.runtime.ScalaRunTime$", ({
  hS: 1
}));
var $n_sr_ScalaRunTime$;
function $m_sr_ScalaRunTime$() {
  if ((!$n_sr_ScalaRunTime$)) {
    $n_sr_ScalaRunTime$ = new $c_sr_ScalaRunTime$();
  }
  return $n_sr_ScalaRunTime$;
}
/** @constructor */
function $c_sr_Statics$() {
}
$p = $c_sr_Statics$.prototype = new $h_O();
$p.constructor = $c_sr_Statics$;
/** @constructor */
function $h_sr_Statics$() {
}
$h_sr_Statics$.prototype = $p;
$p.w = (function(hash, data) {
  var h = this.cY(hash, data);
  var i = h;
  h = ((i << 13) | ((i >>> 19) | 0));
  return ((Math.imul(5, h) - 430675100) | 0);
});
$p.cY = (function(hash, data) {
  var k = data;
  k = Math.imul((-862048943), k);
  var i = k;
  k = ((i << 15) | ((i >>> 17) | 0));
  k = Math.imul(461845907, k);
  return (hash ^ k);
});
$p.ar = (function(hash, length) {
  return this.pi((hash ^ length));
});
$p.pi = (function(h0) {
  var h = h0;
  h = (h ^ ((h >>> 16) | 0));
  h = Math.imul((-2048144789), h);
  h = (h ^ ((h >>> 13) | 0));
  h = Math.imul((-1028477387), h);
  h = (h ^ ((h >>> 16) | 0));
  return h;
});
$p.nO = (function(lv_$_lo, lv_$_hi) {
  return ((lv_$_hi === (lv_$_lo >> 31)) ? lv_$_lo : (lv_$_lo ^ lv_$_hi));
});
$p.pO = (function(dv) {
  var iv = $doubleToInt(dv);
  if ((iv === dv)) {
    return iv;
  } else {
    var $x_1 = $m_RTLong$().h6(dv);
    var lv_$_lo = $x_1.l;
    var lv_$_hi = $x_1.h;
    if ((((4.294967296E9 * lv_$_hi) + (lv_$_lo >>> 0.0)) === dv)) {
      return (lv_$_lo ^ lv_$_hi);
    } else {
      var valueInt = (dv | 0);
      if (((valueInt === dv) && ((1.0 / dv) !== (-Infinity)))) {
        return valueInt;
      } else if ((dv !== dv)) {
        return 2146959360;
      } else {
        var fpBitsDataView = $fpBitsDataView;
        fpBitsDataView.setFloat64(0, dv, true);
        return ((fpBitsDataView.getInt32(0, true) | 0) ^ (fpBitsDataView.getInt32(4, true) | 0));
      }
    }
  }
});
$p.C = (function(x) {
  if ((x === null)) {
    return 0;
  } else if (((typeof x) === "number")) {
    return this.pO((+x));
  } else if ((x instanceof $Long)) {
    var $x_1 = $uJ(x);
    return this.nO($x_1.l, $x_1.h);
  } else {
    return $dp_hashCode__I(x);
  }
});
$p.qr = (function(n) {
  throw $ct_jl_IndexOutOfBoundsException__T__(new $c_jl_IndexOutOfBoundsException(), ("" + n));
});
var $d_sr_Statics$ = new $TypeData().i($c_sr_Statics$, "scala.runtime.Statics$", ({
  hU: 1
}));
var $n_sr_Statics$;
function $m_sr_Statics$() {
  if ((!$n_sr_Statics$)) {
    $n_sr_Statics$ = new $c_sr_Statics$();
  }
  return $n_sr_Statics$;
}
/** @constructor */
function $c_sr_Statics$PFMarker$() {
}
$p = $c_sr_Statics$PFMarker$.prototype = new $h_O();
$p.constructor = $c_sr_Statics$PFMarker$;
/** @constructor */
function $h_sr_Statics$PFMarker$() {
}
$h_sr_Statics$PFMarker$.prototype = $p;
var $d_sr_Statics$PFMarker$ = new $TypeData().i($c_sr_Statics$PFMarker$, "scala.runtime.Statics$PFMarker$", ({
  hV: 1
}));
var $n_sr_Statics$PFMarker$;
function $m_sr_Statics$PFMarker$() {
  if ((!$n_sr_Statics$PFMarker$)) {
    $n_sr_Statics$PFMarker$ = new $c_sr_Statics$PFMarker$();
  }
  return $n_sr_Statics$PFMarker$;
}
/** @constructor */
function $c_sjs_concurrent_JSExecutionContext$() {
  this.mL = null;
  $n_sjs_concurrent_JSExecutionContext$ = this;
  this.mL = $m_sjs_concurrent_QueueExecutionContext$().pf();
}
$p = $c_sjs_concurrent_JSExecutionContext$.prototype = new $h_O();
$p.constructor = $c_sjs_concurrent_JSExecutionContext$;
/** @constructor */
function $h_sjs_concurrent_JSExecutionContext$() {
}
$h_sjs_concurrent_JSExecutionContext$.prototype = $p;
var $d_sjs_concurrent_JSExecutionContext$ = new $TypeData().i($c_sjs_concurrent_JSExecutionContext$, "scala.scalajs.concurrent.JSExecutionContext$", ({
  hW: 1
}));
var $n_sjs_concurrent_JSExecutionContext$;
function $m_sjs_concurrent_JSExecutionContext$() {
  if ((!$n_sjs_concurrent_JSExecutionContext$)) {
    $n_sjs_concurrent_JSExecutionContext$ = new $c_sjs_concurrent_JSExecutionContext$();
  }
  return $n_sjs_concurrent_JSExecutionContext$;
}
/** @constructor */
function $c_sjs_concurrent_QueueExecutionContext$() {
}
$p = $c_sjs_concurrent_QueueExecutionContext$.prototype = new $h_O();
$p.constructor = $c_sjs_concurrent_QueueExecutionContext$;
/** @constructor */
function $h_sjs_concurrent_QueueExecutionContext$() {
}
$h_sjs_concurrent_QueueExecutionContext$.prototype = $p;
$p.pf = (function() {
  return (((typeof Promise) === "undefined") ? new $c_sjs_concurrent_QueueExecutionContext$TimeoutsExecutionContext() : new $c_sjs_concurrent_QueueExecutionContext$PromisesExecutionContext());
});
var $d_sjs_concurrent_QueueExecutionContext$ = new $TypeData().i($c_sjs_concurrent_QueueExecutionContext$, "scala.scalajs.concurrent.QueueExecutionContext$", ({
  hX: 1
}));
var $n_sjs_concurrent_QueueExecutionContext$;
function $m_sjs_concurrent_QueueExecutionContext$() {
  if ((!$n_sjs_concurrent_QueueExecutionContext$)) {
    $n_sjs_concurrent_QueueExecutionContext$ = new $c_sjs_concurrent_QueueExecutionContext$();
  }
  return $n_sjs_concurrent_QueueExecutionContext$;
}
/** @constructor */
function $c_sjs_js_Thenable$ThenableOps$() {
}
$p = $c_sjs_js_Thenable$ThenableOps$.prototype = new $h_O();
$p.constructor = $c_sjs_js_Thenable$ThenableOps$;
/** @constructor */
function $h_sjs_js_Thenable$ThenableOps$() {
}
$h_sjs_js_Thenable$ThenableOps$.prototype = $p;
$p.hm = (function(this$) {
  var p2 = $ct_s_concurrent_impl_Promise$DefaultPromise__(new $c_s_concurrent_impl_Promise$DefaultPromise());
  this$.then(((arg1$2) => {
    $f_s_concurrent_Promise__success__O__s_concurrent_Promise(p2, arg1$2);
  }), $m_sjs_js_defined$().na(((arg1$2$1) => {
    $f_s_concurrent_Promise__failure__jl_Throwable__s_concurrent_Promise(p2, ((arg1$2$1 instanceof $c_jl_Throwable) ? arg1$2$1 : new $c_sjs_js_JavaScriptException(arg1$2$1)));
  })));
  return p2;
});
var $d_sjs_js_Thenable$ThenableOps$ = new $TypeData().i($c_sjs_js_Thenable$ThenableOps$, "scala.scalajs.js.Thenable$ThenableOps$", ({
  i3: 1
}));
var $n_sjs_js_Thenable$ThenableOps$;
function $m_sjs_js_Thenable$ThenableOps$() {
  if ((!$n_sjs_js_Thenable$ThenableOps$)) {
    $n_sjs_js_Thenable$ThenableOps$ = new $c_sjs_js_Thenable$ThenableOps$();
  }
  return $n_sjs_js_Thenable$ThenableOps$;
}
/** @constructor */
function $c_sjs_js_defined$() {
}
$p = $c_sjs_js_defined$.prototype = new $h_O();
$p.constructor = $c_sjs_js_defined$;
/** @constructor */
function $h_sjs_js_defined$() {
}
$h_sjs_js_defined$.prototype = $p;
$p.na = (function(a) {
  return a;
});
var $d_sjs_js_defined$ = new $TypeData().i($c_sjs_js_defined$, "scala.scalajs.js.defined$", ({
  i6: 1
}));
var $n_sjs_js_defined$;
function $m_sjs_js_defined$() {
  if ((!$n_sjs_js_defined$)) {
    $n_sjs_js_defined$ = new $c_sjs_js_defined$();
  }
  return $n_sjs_js_defined$;
}
/** @constructor */
function $c_sjs_js_timers_package$() {
}
$p = $c_sjs_js_timers_package$.prototype = new $h_O();
$p.constructor = $c_sjs_js_timers_package$;
/** @constructor */
function $h_sjs_js_timers_package$() {
}
$h_sjs_js_timers_package$.prototype = $p;
$p.rf = (function(interval, body) {
  return setTimeout((() => {
    body.F();
  }), interval);
});
var $d_sjs_js_timers_package$ = new $TypeData().i($c_sjs_js_timers_package$, "scala.scalajs.js.timers.package$", ({
  i7: 1
}));
var $n_sjs_js_timers_package$;
function $m_sjs_js_timers_package$() {
  if ((!$n_sjs_js_timers_package$)) {
    $n_sjs_js_timers_package$ = new $c_sjs_js_timers_package$();
  }
  return $n_sjs_js_timers_package$;
}
/** @constructor */
function $c_sjsr_Compat$() {
}
$p = $c_sjsr_Compat$.prototype = new $h_O();
$p.constructor = $c_sjsr_Compat$;
/** @constructor */
function $h_sjsr_Compat$() {
}
$h_sjsr_Compat$.prototype = $p;
$p.rz = (function(seq) {
  if ((seq instanceof $c_sjsr_WrappedVarArgs)) {
    return seq.gQ;
  } else {
    var result = [];
    seq.bm(new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((x$2$2) => (result.push(x$2$2) | 0))));
    return result;
  }
});
var $d_sjsr_Compat$ = new $TypeData().i($c_sjsr_Compat$, "scala.scalajs.runtime.Compat$", ({
  ij: 1
}));
var $n_sjsr_Compat$;
function $m_sjsr_Compat$() {
  if ((!$n_sjsr_Compat$)) {
    $n_sjsr_Compat$ = new $c_sjsr_Compat$();
  }
  return $n_sjsr_Compat$;
}
function $f_s_util_control_NoStackTrace__fillInStackTrace__jl_Throwable($thiz) {
  return ($m_s_util_control_NoStackTrace$().mS ? $c_jl_Throwable.prototype.eP.call($thiz) : $thiz);
}
/** @constructor */
function $c_s_util_control_NoStackTrace$() {
  this.mS = false;
  this.mS = false;
}
$p = $c_s_util_control_NoStackTrace$.prototype = new $h_O();
$p.constructor = $c_s_util_control_NoStackTrace$;
/** @constructor */
function $h_s_util_control_NoStackTrace$() {
}
$h_s_util_control_NoStackTrace$.prototype = $p;
var $d_s_util_control_NoStackTrace$ = new $TypeData().i($c_s_util_control_NoStackTrace$, "scala.util.control.NoStackTrace$", ({
  im: 1
}));
var $n_s_util_control_NoStackTrace$;
function $m_s_util_control_NoStackTrace$() {
  if ((!$n_s_util_control_NoStackTrace$)) {
    $n_s_util_control_NoStackTrace$ = new $c_s_util_control_NoStackTrace$();
  }
  return $n_s_util_control_NoStackTrace$;
}
/** @constructor */
function $c_s_util_control_NonFatal$() {
}
$p = $c_s_util_control_NonFatal$.prototype = new $h_O();
$p.constructor = $c_s_util_control_NonFatal$;
/** @constructor */
function $h_s_util_control_NonFatal$() {
}
$h_s_util_control_NonFatal$.prototype = $p;
$p.gW = (function(t) {
  matchAlts1: {
    matchAlts2: {
      if ((t instanceof $c_jl_VirtualMachineError)) {
        break matchAlts2;
      }
      if (false) {
        break matchAlts2;
      }
      if (false) {
        break matchAlts2;
      }
      if (false) {
        break matchAlts2;
      }
      if (false) {
        break matchAlts2;
      }
      break matchAlts1;
    }
    return false;
  }
  return true;
});
$p.dF = (function(t) {
  return (this.gW(t) ? new $c_s_Some(t) : $m_s_None$());
});
var $d_s_util_control_NonFatal$ = new $TypeData().i($c_s_util_control_NonFatal$, "scala.util.control.NonFatal$", ({
  io: 1
}));
var $n_s_util_control_NonFatal$;
function $m_s_util_control_NonFatal$() {
  if ((!$n_s_util_control_NonFatal$)) {
    $n_s_util_control_NonFatal$ = new $c_s_util_control_NonFatal$();
  }
  return $n_s_util_control_NonFatal$;
}
/** @constructor */
function $c_s_util_hashing_MurmurHash3() {
}
$p = $c_s_util_hashing_MurmurHash3.prototype = new $h_O();
$p.constructor = $c_s_util_hashing_MurmurHash3;
/** @constructor */
function $h_s_util_hashing_MurmurHash3() {
}
$h_s_util_hashing_MurmurHash3.prototype = $p;
$p.w = (function(hash, data) {
  var h = this.cY(hash, data);
  var i = h;
  h = ((i << 13) | ((i >>> 19) | 0));
  return ((Math.imul(5, h) - 430675100) | 0);
});
$p.cY = (function(hash, data) {
  var k = data;
  k = Math.imul((-862048943), k);
  var i = k;
  k = ((i << 15) | ((i >>> 17) | 0));
  k = Math.imul(461845907, k);
  return (hash ^ k);
});
$p.ar = (function(hash, length) {
  return this.ge((hash ^ length));
});
$p.ge = (function(hash) {
  var h = hash;
  h = (h ^ ((h >>> 16) | 0));
  h = Math.imul((-2048144789), h);
  h = (h ^ ((h >>> 13) | 0));
  h = Math.imul((-1028477387), h);
  h = (h ^ ((h >>> 16) | 0));
  return h;
});
$p.ok = (function(x, y, seed) {
  var h = seed;
  h = this.w(h, $f_T__hashCode__I("Tuple2"));
  h = this.w(h, x);
  h = this.w(h, y);
  return this.ar(h, 2);
});
$p.e7 = (function(x, seed, ignorePrefix) {
  var arr = x.aN();
  if ((arr === 0)) {
    return ((!ignorePrefix) ? $f_T__hashCode__I(x.aP()) : seed);
  } else {
    var h = seed;
    if ((!ignorePrefix)) {
      h = this.w(h, $f_T__hashCode__I(x.aP()));
    }
    var i = 0;
    while ((i < arr)) {
      h = this.w(h, $m_sr_Statics$().C(x.aO(i)));
      i = ((1 + i) | 0);
    }
    return this.ar(h, arr);
  }
});
$p.h0 = (function(x, seed, caseClassName) {
  var arr = x.aN();
  var aye = $f_T__hashCode__I(((caseClassName !== null) ? caseClassName : x.aP()));
  if ((arr === 0)) {
    return aye;
  } else {
    var h = seed;
    h = this.w(h, aye);
    var i = 0;
    while ((i < arr)) {
      h = this.w(h, $m_sr_Statics$().C(x.aO(i)));
      i = ((1 + i) | 0);
    }
    return this.ar(h, arr);
  }
});
$p.jv = (function(xs, seed) {
  var a = 0;
  var b = 0;
  var n = 0;
  var c = 1;
  var iterator = xs.i();
  while (iterator.m()) {
    var x = iterator.g();
    var h = $m_sr_Statics$().C(x);
    a = ((a + h) | 0);
    b = (b ^ h);
    c = Math.imul(c, (1 | h));
    n = ((1 + n) | 0);
  }
  var h$2 = seed;
  h$2 = this.w(h$2, a);
  h$2 = this.w(h$2, b);
  h$2 = this.cY(h$2, c);
  return this.ar(h$2, n);
});
$p.qM = (function(xs, seed) {
  var it = xs.i();
  var h = seed;
  if ((!it.m())) {
    return this.ar(h, 0);
  }
  var x0 = it.g();
  if ((!it.m())) {
    return this.ar(this.w(h, $m_sr_Statics$().C(x0)), 1);
  }
  var x1 = it.g();
  var initial = $m_sr_Statics$().C(x0);
  h = this.w(h, initial);
  var h0 = h;
  var prev = $m_sr_Statics$().C(x1);
  var rangeDiff = ((prev - initial) | 0);
  var i = 2;
  while (it.m()) {
    h = this.w(h, prev);
    var hash = $m_sr_Statics$().C(it.g());
    if (((rangeDiff !== ((hash - prev) | 0)) || (rangeDiff === 0))) {
      h = this.w(h, hash);
      i = ((1 + i) | 0);
      while (it.m()) {
        h = this.w(h, $m_sr_Statics$().C(it.g()));
        i = ((1 + i) | 0);
      }
      return this.ar(h, i);
    }
    prev = hash;
    i = ((1 + i) | 0);
  }
  return this.ge(this.w(this.w(h0, rangeDiff), prev));
});
$p.aB = (function(a, seed) {
  var h = seed;
  var l = $m_jl_reflect_Array$().bJ(a);
  switch (l) {
    case 0: {
      return this.ar(h, 0);
      break;
    }
    case 1: {
      return this.ar(this.w(h, $m_sr_Statics$().C($m_sr_ScalaRunTime$().dZ(a, 0))), 1);
      break;
    }
    default: {
      var initial = $m_sr_Statics$().C($m_sr_ScalaRunTime$().dZ(a, 0));
      h = this.w(h, initial);
      var h0 = h;
      var prev = $m_sr_Statics$().C($m_sr_ScalaRunTime$().dZ(a, 1));
      var rangeDiff = ((prev - initial) | 0);
      var i = 2;
      while ((i < l)) {
        h = this.w(h, prev);
        var hash = $m_sr_Statics$().C($m_sr_ScalaRunTime$().dZ(a, i));
        if (((rangeDiff !== ((hash - prev) | 0)) || (rangeDiff === 0))) {
          h = this.w(h, hash);
          i = ((1 + i) | 0);
          while ((i < l)) {
            h = this.w(h, $m_sr_Statics$().C($m_sr_ScalaRunTime$().dZ(a, i)));
            i = ((1 + i) | 0);
          }
          return this.ar(h, l);
        }
        prev = hash;
        i = ((1 + i) | 0);
      }
      return this.ge(this.w(this.w(h0, rangeDiff), prev));
    }
  }
});
$p.qS = (function(start, step, last, seed) {
  return this.ge(this.w(this.w(this.w(seed, start), step), last));
});
$p.ql = (function(a, seed) {
  var h = seed;
  var l = a.q();
  switch (l) {
    case 0: {
      return this.ar(h, 0);
      break;
    }
    case 1: {
      return this.ar(this.w(h, $m_sr_Statics$().C(a.v(0))), 1);
      break;
    }
    default: {
      var initial = $m_sr_Statics$().C(a.v(0));
      h = this.w(h, initial);
      var h0 = h;
      var prev = $m_sr_Statics$().C(a.v(1));
      var rangeDiff = ((prev - initial) | 0);
      var i = 2;
      while ((i < l)) {
        h = this.w(h, prev);
        var hash = $m_sr_Statics$().C(a.v(i));
        if (((rangeDiff !== ((hash - prev) | 0)) || (rangeDiff === 0))) {
          h = this.w(h, hash);
          i = ((1 + i) | 0);
          while ((i < l)) {
            h = this.w(h, $m_sr_Statics$().C(a.v(i)));
            i = ((1 + i) | 0);
          }
          return this.ar(h, l);
        }
        prev = hash;
        i = ((1 + i) | 0);
      }
      return this.ge(this.w(this.w(h0, rangeDiff), prev));
    }
  }
});
$p.qx = (function(xs, seed) {
  var n = 0;
  var h = seed;
  var rangeState = 0;
  var rangeDiff = 0;
  var prev = 0;
  var initial = 0;
  var elems = xs;
  while ((!elems.c())) {
    var head = elems.n();
    var tail = elems.l();
    var hash = $m_sr_Statics$().C(head);
    h = this.w(h, hash);
    switch (rangeState) {
      case 0: {
        initial = hash;
        rangeState = 1;
        break;
      }
      case 1: {
        rangeDiff = ((hash - prev) | 0);
        rangeState = 2;
        break;
      }
      case 2: {
        if (((rangeDiff !== ((hash - prev) | 0)) || (rangeDiff === 0))) {
          rangeState = 3;
        }
        break;
      }
    }
    prev = hash;
    n = ((1 + n) | 0);
    elems = tail;
  }
  return ((rangeState === 2) ? this.qS(initial, rangeDiff, prev, seed) : this.ar(h, n));
});
function $f_Lcom_raquo_airstream_common_InternalNextErrorObserver__onTry__s_util_Try__Lcom_raquo_airstream_core_Transaction__V($thiz, nextValue, transaction) {
  nextValue.c8(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((_$1) => {
    $f_Lcom_raquo_airstream_core_WritableStream__fireError__jl_Throwable__Lcom_raquo_airstream_core_Transaction__V($thiz, _$1, transaction);
  })), new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((_$2) => {
    $thiz.jl(_$2, transaction);
  })));
}
function $f_Lcom_raquo_airstream_common_InternalTryObserver__onNext__O__Lcom_raquo_airstream_core_Transaction__V($thiz, nextValue, transaction) {
  $thiz.hh(new $c_s_util_Success(nextValue), transaction);
}
function $f_Lcom_raquo_airstream_common_InternalTryObserver__onError__jl_Throwable__Lcom_raquo_airstream_core_Transaction__V($thiz, nextError, transaction) {
  $thiz.hh(new $c_s_util_Failure(nextError), transaction);
}
/** @constructor */
function $c_Lcom_raquo_airstream_ownership_OneTimeOwner(onAccessAfterKilled) {
  this.k8 = null;
  this.k7 = null;
  this.hz = false;
  this.k7 = onAccessAfterKilled;
  $f_Lcom_raquo_airstream_ownership_Owner__$init$__V(this);
  this.hz = false;
}
$p = $c_Lcom_raquo_airstream_ownership_OneTimeOwner.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_airstream_ownership_OneTimeOwner;
/** @constructor */
function $h_Lcom_raquo_airstream_ownership_OneTimeOwner() {
}
$h_Lcom_raquo_airstream_ownership_OneTimeOwner.prototype = $p;
$p.eX = (function() {
  return this.k8;
});
$p.nf = (function(x$0) {
  this.k8 = x$0;
});
$p.o1 = (function(subscription) {
  if (this.hz) {
    $p_Lcom_raquo_airstream_ownership_Subscription__safeCleanup__V(subscription);
    this.k7.F();
  } else {
    $f_Lcom_raquo_airstream_ownership_Owner__own__Lcom_raquo_airstream_ownership_Subscription__V(this, subscription);
  }
});
$p.nM = (function() {
  $f_Lcom_raquo_airstream_ownership_Owner__killSubscriptions__V(this);
  this.hz = true;
});
var $d_Lcom_raquo_airstream_ownership_OneTimeOwner = new $TypeData().i($c_Lcom_raquo_airstream_ownership_OneTimeOwner, "com.raquo.airstream.ownership.OneTimeOwner", ({
  d2: 1,
  bb: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_api_Laminar$unsafeWindowOwner$(outer) {
  this.ku = null;
  if ((outer === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
  $f_Lcom_raquo_airstream_ownership_Owner__$init$__V(this);
}
$p = $c_Lcom_raquo_laminar_api_Laminar$unsafeWindowOwner$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_api_Laminar$unsafeWindowOwner$;
/** @constructor */
function $h_Lcom_raquo_laminar_api_Laminar$unsafeWindowOwner$() {
}
$h_Lcom_raquo_laminar_api_Laminar$unsafeWindowOwner$.prototype = $p;
$p.eX = (function() {
  return this.ku;
});
$p.nf = (function(x$0) {
  this.ku = x$0;
});
$p.nM = (function() {
  $f_Lcom_raquo_airstream_ownership_Owner__killSubscriptions__V(this);
});
$p.o1 = (function(subscription) {
  $f_Lcom_raquo_airstream_ownership_Owner__own__Lcom_raquo_airstream_ownership_Subscription__V(this, subscription);
});
var $d_Lcom_raquo_laminar_api_Laminar$unsafeWindowOwner$ = new $TypeData().i($c_Lcom_raquo_laminar_api_Laminar$unsafeWindowOwner$, "com.raquo.laminar.api.Laminar$unsafeWindowOwner$", ({
  dm: 1,
  bb: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_codecs_package$$anon$2(outer) {
  if ((outer === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
}
$p = $c_Lcom_raquo_laminar_codecs_package$$anon$2.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_codecs_package$$anon$2;
/** @constructor */
function $h_Lcom_raquo_laminar_codecs_package$$anon$2() {
}
$h_Lcom_raquo_laminar_codecs_package$$anon$2.prototype = $p;
$p.g1 = (function(scalaValue) {
  return scalaValue;
});
$p.iR = (function(domValue) {
  return domValue;
});
var $d_Lcom_raquo_laminar_codecs_package$$anon$2 = new $TypeData().i($c_Lcom_raquo_laminar_codecs_package$$anon$2, "com.raquo.laminar.codecs.package$$anon$2", ({
  dt: 1,
  be: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_keys_CompositeKey(name, getRawDomValue, setRawDomValue, separator) {
  this.lv = null;
  this.lx = null;
  this.lw = null;
  this.hJ = null;
  this.lv = getRawDomValue;
  this.lx = setRawDomValue;
  this.lw = separator;
  this.hJ = new $c_Lcom_raquo_laminar_keys_CompositeKey$CompositeCodec(separator);
}
$p = $c_Lcom_raquo_laminar_keys_CompositeKey.prototype = new $h_Lcom_raquo_laminar_keys_Key();
$p.constructor = $c_Lcom_raquo_laminar_keys_CompositeKey;
/** @constructor */
function $h_Lcom_raquo_laminar_keys_CompositeKey() {
}
$h_Lcom_raquo_laminar_keys_CompositeKey.prototype = $p;
$p.eJ = (function(items) {
  return new $c_Lcom_raquo_laminar_modifiers_CompositeKeySetter(this, ($m_Lcom_raquo_laminar_api_package$().o.oQ(), $m_Lcom_raquo_laminar_keys_CompositeKey$().nT(items, this.lw)));
});
var $d_Lcom_raquo_laminar_keys_CompositeKey = new $TypeData().i($c_Lcom_raquo_laminar_keys_CompositeKey, "com.raquo.laminar.keys.CompositeKey", ({
  dM: 1,
  ak: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_keys_CompositeKey$CompositeCodec(separator) {
  this.hK = null;
  this.hK = separator;
}
$p = $c_Lcom_raquo_laminar_keys_CompositeKey$CompositeCodec.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_keys_CompositeKey$CompositeCodec;
/** @constructor */
function $h_Lcom_raquo_laminar_keys_CompositeKey$CompositeCodec() {
}
$h_Lcom_raquo_laminar_keys_CompositeKey$CompositeCodec.prototype = $p;
$p.nk = (function(domValue) {
  return $m_Lcom_raquo_laminar_keys_CompositeKey$().nT(domValue, this.hK);
});
$p.nn = (function(scalaValue) {
  return $f_sc_IterableOnceOps__mkString__T__T__T__T(scalaValue, "", this.hK, "");
});
$p.iR = (function(domValue) {
  return this.nk(domValue);
});
$p.g1 = (function(scalaValue) {
  return this.nn(scalaValue);
});
var $d_Lcom_raquo_laminar_keys_CompositeKey$CompositeCodec = new $TypeData().i($c_Lcom_raquo_laminar_keys_CompositeKey$CompositeCodec, "com.raquo.laminar.keys.CompositeKey$CompositeCodec", ({
  dO: 1,
  be: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_keys_CompositeKey$CompositeValueMappers$StringValueMapper$(outer) {
  if ((outer === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
}
$p = $c_Lcom_raquo_laminar_keys_CompositeKey$CompositeValueMappers$StringValueMapper$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_keys_CompositeKey$CompositeValueMappers$StringValueMapper$;
/** @constructor */
function $h_Lcom_raquo_laminar_keys_CompositeKey$CompositeValueMappers$StringValueMapper$() {
}
$h_Lcom_raquo_laminar_keys_CompositeKey$CompositeValueMappers$StringValueMapper$.prototype = $p;
var $d_Lcom_raquo_laminar_keys_CompositeKey$CompositeValueMappers$StringValueMapper$ = new $TypeData().i($c_Lcom_raquo_laminar_keys_CompositeKey$CompositeValueMappers$StringValueMapper$, "com.raquo.laminar.keys.CompositeKey$CompositeValueMappers$StringValueMapper$", ({
  dQ: 1,
  dP: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_keys_EventProp(name) {
  this.f9 = null;
  this.f9 = name;
}
$p = $c_Lcom_raquo_laminar_keys_EventProp.prototype = new $h_Lcom_raquo_laminar_keys_Key();
$p.constructor = $c_Lcom_raquo_laminar_keys_EventProp;
/** @constructor */
function $h_Lcom_raquo_laminar_keys_EventProp() {
}
$h_Lcom_raquo_laminar_keys_EventProp.prototype = $p;
var $d_Lcom_raquo_laminar_keys_EventProp = new $TypeData().i($c_Lcom_raquo_laminar_keys_EventProp, "com.raquo.laminar.keys.EventProp", ({
  dT: 1,
  ak: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_keys_HtmlAttr(name, codec) {
  this.fa = null;
  this.hM = null;
  this.fa = name;
  this.hM = codec;
}
$p = $c_Lcom_raquo_laminar_keys_HtmlAttr.prototype = new $h_Lcom_raquo_laminar_keys_Key();
$p.constructor = $c_Lcom_raquo_laminar_keys_HtmlAttr;
/** @constructor */
function $h_Lcom_raquo_laminar_keys_HtmlAttr() {
}
$h_Lcom_raquo_laminar_keys_HtmlAttr.prototype = $p;
var $d_Lcom_raquo_laminar_keys_HtmlAttr = new $TypeData().i($c_Lcom_raquo_laminar_keys_HtmlAttr, "com.raquo.laminar.keys.HtmlAttr", ({
  dU: 1,
  ak: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_keys_HtmlProp(name, codec) {
  this.cB = null;
  this.hN = null;
  this.cB = name;
  this.hN = codec;
}
$p = $c_Lcom_raquo_laminar_keys_HtmlProp.prototype = new $h_Lcom_raquo_laminar_keys_Key();
$p.constructor = $c_Lcom_raquo_laminar_keys_HtmlProp;
/** @constructor */
function $h_Lcom_raquo_laminar_keys_HtmlProp() {
}
$h_Lcom_raquo_laminar_keys_HtmlProp.prototype = $p;
$p.mV = (function(value) {
  return new $c_Lcom_raquo_laminar_modifiers_KeySetter(this, value, new $c_sjsr_AnonFunction3_$$Lambda$73f37e31ba038fe839c174212837da323f140c96(((element, prop, value$2) => {
    $m_Lcom_raquo_laminar_DomApi$().od(element, prop, value$2);
  })));
});
$p.mW = (function(values) {
  var update = ((this.cB === "value") ? new $c_sjsr_AnonFunction3_$$Lambda$73f37e31ba038fe839c174212837da323f140c96(((element, nextValue, reason) => {
    var nextDomValue = this.hN.g1(nextValue);
    var x = $m_Lcom_raquo_laminar_DomApi$().qb(element, this);
    if ((!((x !== (void 0)) && $m_sr_BoxesRunTime$().j(nextDomValue, x)))) {
      $m_Lcom_raquo_laminar_DomApi$().oe(element, this, nextDomValue);
    }
  })) : new $c_sjsr_AnonFunction3_$$Lambda$73f37e31ba038fe839c174212837da323f140c96(((element$2, nextValue$2, reason$2) => {
    $m_Lcom_raquo_laminar_DomApi$().od(element$2, this, nextValue$2);
  })));
  return new $c_Lcom_raquo_laminar_modifiers_KeyUpdater(this, values.gi(), update);
});
function $isArrayOf_Lcom_raquo_laminar_keys_HtmlProp(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.bh)));
}
var $d_Lcom_raquo_laminar_keys_HtmlProp = new $TypeData().i($c_Lcom_raquo_laminar_keys_HtmlProp, "com.raquo.laminar.keys.HtmlProp", ({
  bh: 1,
  ak: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_keys_SvgAttr(localName, codec, namespacePrefix) {
  this.hP = null;
  this.hO = null;
  this.gx = null;
  this.gy = null;
  this.hP = localName;
  this.hO = codec;
  var this$2 = (namespacePrefix.c() ? $m_s_None$() : new $c_s_Some(((namespacePrefix.s() + ":") + localName)));
  this.gx = (this$2.c() ? localName : this$2.s());
  this.gy = (namespacePrefix.c() ? $m_s_None$() : new $c_s_Some($m_Lcom_raquo_laminar_keys_SvgAttr$().qD(namespacePrefix.s())));
}
$p = $c_Lcom_raquo_laminar_keys_SvgAttr.prototype = new $h_Lcom_raquo_laminar_keys_Key();
$p.constructor = $c_Lcom_raquo_laminar_keys_SvgAttr;
/** @constructor */
function $h_Lcom_raquo_laminar_keys_SvgAttr() {
}
$h_Lcom_raquo_laminar_keys_SvgAttr.prototype = $p;
var $d_Lcom_raquo_laminar_keys_SvgAttr = new $TypeData().i($c_Lcom_raquo_laminar_keys_SvgAttr, "com.raquo.laminar.keys.SvgAttr", ({
  dV: 1,
  ak: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_modifiers_Modifier$$anon$1() {
}
$p = $c_Lcom_raquo_laminar_modifiers_Modifier$$anon$1.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_modifiers_Modifier$$anon$1;
/** @constructor */
function $h_Lcom_raquo_laminar_modifiers_Modifier$$anon$1() {
}
$h_Lcom_raquo_laminar_modifiers_Modifier$$anon$1.prototype = $p;
$p.co = (function(element) {
});
var $d_Lcom_raquo_laminar_modifiers_Modifier$$anon$1 = new $TypeData().i($c_Lcom_raquo_laminar_modifiers_Modifier$$anon$1, "com.raquo.laminar.modifiers.Modifier$$anon$1", ({
  e3: 1,
  X: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_modifiers_Modifier$$anon$2(f$2, outer) {
  this.lG = null;
  this.lG = f$2;
  if ((outer === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
}
$p = $c_Lcom_raquo_laminar_modifiers_Modifier$$anon$2.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_modifiers_Modifier$$anon$2;
/** @constructor */
function $h_Lcom_raquo_laminar_modifiers_Modifier$$anon$2() {
}
$h_Lcom_raquo_laminar_modifiers_Modifier$$anon$2.prototype = $p;
$p.co = (function(element) {
  var this$2 = $m_Lcom_raquo_airstream_core_Transaction$onStart$();
  var f = (() => {
    this.lG.b(element);
  });
  $m_Lcom_raquo_airstream_core_Transaction$onStart$();
  var when = true;
  if ((this$2.aY || (!when))) {
    f();
  } else {
    this$2.aY = true;
    try {
      f();
    } finally {
      this$2.aY = false;
      $p_Lcom_raquo_airstream_core_Transaction$onStart$__resolve__V(this$2);
    }
  }
});
var $d_Lcom_raquo_laminar_modifiers_Modifier$$anon$2 = new $TypeData().i($c_Lcom_raquo_laminar_modifiers_Modifier$$anon$2, "com.raquo.laminar.modifiers.Modifier$$anon$2", ({
  e4: 1,
  X: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_modifiers_RenderableNode$$anon$1() {
}
$p = $c_Lcom_raquo_laminar_modifiers_RenderableNode$$anon$1.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_modifiers_RenderableNode$$anon$1;
/** @constructor */
function $h_Lcom_raquo_laminar_modifiers_RenderableNode$$anon$1() {
}
$h_Lcom_raquo_laminar_modifiers_RenderableNode$$anon$1.prototype = $p;
var $d_Lcom_raquo_laminar_modifiers_RenderableNode$$anon$1 = new $TypeData().i($c_Lcom_raquo_laminar_modifiers_RenderableNode$$anon$1, "com.raquo.laminar.modifiers.RenderableNode$$anon$1", ({
  e7: 1,
  e5: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_modifiers_RenderableSeq$collectionSeqRenderable$() {
}
$p = $c_Lcom_raquo_laminar_modifiers_RenderableSeq$collectionSeqRenderable$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_modifiers_RenderableSeq$collectionSeqRenderable$;
/** @constructor */
function $h_Lcom_raquo_laminar_modifiers_RenderableSeq$collectionSeqRenderable$() {
}
$h_Lcom_raquo_laminar_modifiers_RenderableSeq$collectionSeqRenderable$.prototype = $p;
var $d_Lcom_raquo_laminar_modifiers_RenderableSeq$collectionSeqRenderable$ = new $TypeData().i($c_Lcom_raquo_laminar_modifiers_RenderableSeq$collectionSeqRenderable$, "com.raquo.laminar.modifiers.RenderableSeq$collectionSeqRenderable$", ({
  e9: 1,
  e8: 1
}));
var $n_Lcom_raquo_laminar_modifiers_RenderableSeq$collectionSeqRenderable$;
function $m_Lcom_raquo_laminar_modifiers_RenderableSeq$collectionSeqRenderable$() {
  if ((!$n_Lcom_raquo_laminar_modifiers_RenderableSeq$collectionSeqRenderable$)) {
    $n_Lcom_raquo_laminar_modifiers_RenderableSeq$collectionSeqRenderable$ = new $c_Lcom_raquo_laminar_modifiers_RenderableSeq$collectionSeqRenderable$();
  }
  return $n_Lcom_raquo_laminar_modifiers_RenderableSeq$collectionSeqRenderable$;
}
/** @constructor */
function $c_Lcom_raquo_laminar_modifiers_RenderableText$$anon$1(render$2, outer) {
  this.lH = null;
  this.lH = render$2;
  if ((outer === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
}
$p = $c_Lcom_raquo_laminar_modifiers_RenderableText$$anon$1.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_modifiers_RenderableText$$anon$1;
/** @constructor */
function $h_Lcom_raquo_laminar_modifiers_RenderableText$$anon$1() {
}
$h_Lcom_raquo_laminar_modifiers_RenderableText$$anon$1.prototype = $p;
$p.iK = (function(value) {
  return this.lH.b(value);
});
var $d_Lcom_raquo_laminar_modifiers_RenderableText$$anon$1 = new $TypeData().i($c_Lcom_raquo_laminar_modifiers_RenderableText$$anon$1, "com.raquo.laminar.modifiers.RenderableText$$anon$1", ({
  ec: 1,
  ea: 1
}));
function $f_Lcom_raquo_laminar_nodes_ParentNode__$init$__V($thiz) {
  $thiz.ng(new $c_Lcom_raquo_airstream_ownership_DynamicOwner(new $c_sjsr_AnonFunction0_$$Lambda$2bf0f8dc580d6edeb2d6a336c52a1bab3049702d((() => {
    throw $ct_jl_Exception__T__(new $c_jl_Exception(), ("Attempting to use owner of unmounted element: " + $f_sc_IterableOnceOps__mkString__T__T__T__T($m_Lcom_raquo_laminar_DomApi$().pH($thiz.I(), ($m_Lcom_raquo_laminar_DomApi$(), $m_sci_Nil$())), "", " > ", "")));
  }))));
}
/** @constructor */
function $c_Lcom_raquo_laminar_tags_HtmlTag(name, void$1) {
  this.i2 = null;
  this.i2 = name;
}
$p = $c_Lcom_raquo_laminar_tags_HtmlTag.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_tags_HtmlTag;
/** @constructor */
function $h_Lcom_raquo_laminar_tags_HtmlTag() {
}
$h_Lcom_raquo_laminar_tags_HtmlTag.prototype = $p;
$p.ad = (function(modifiers) {
  var element = this.pm();
  modifiers.bm(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((modifier) => {
    modifier.co(element);
  })));
  return element;
});
$p.pm = (function() {
  return new $c_Lcom_raquo_laminar_nodes_ReactiveHtmlElement(this, $m_Lcom_raquo_laminar_DomApi$().pC(this));
});
var $d_Lcom_raquo_laminar_tags_HtmlTag = new $TypeData().i($c_Lcom_raquo_laminar_tags_HtmlTag, "com.raquo.laminar.tags.HtmlTag", ({
  eo: 1,
  bl: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_tags_SvgTag(name, void$1) {
  this.lL = null;
  this.lL = name;
}
$p = $c_Lcom_raquo_laminar_tags_SvgTag.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_tags_SvgTag;
/** @constructor */
function $h_Lcom_raquo_laminar_tags_SvgTag() {
}
$h_Lcom_raquo_laminar_tags_SvgTag.prototype = $p;
var $d_Lcom_raquo_laminar_tags_SvgTag = new $TypeData().i($c_Lcom_raquo_laminar_tags_SvgTag, "com.raquo.laminar.tags.SvgTag", ({
  ep: 1,
  bl: 1
}));
/** @constructor */
function $c_jl_Character$() {
  this.i4 = null;
  $n_jl_Character$ = this;
  this.i4 = $constArrUDiffs_I(67, "1C]4m6m=c4]4]4]4]4]4]4]4]4]3g4]2m9]2m1Jm1m9s4g5mm6]3]4mm12>mEm1m6m1]3]=]DI]1<m24mIs4g2c4w9];]4]<]3m3m=m3mH]8]2m=mBHm3]4mK3{gggg2:g=m@]13]4E]");
}
$p = $c_jl_Character$.prototype = new $h_O();
$p.constructor = $c_jl_Character$;
/** @constructor */
function $h_jl_Character$() {
}
$h_jl_Character$.prototype = $p;
$p.rA = (function(codePoint) {
  if (((codePoint >>> 0) > 1114111)) {
    throw $ct_jl_IllegalArgumentException__(new $c_jl_IllegalArgumentException());
  }
  return String.fromCodePoint(codePoint);
});
$p.pJ = (function(codePoint, radix) {
  if ((codePoint < 256)) {
    var value = (((((codePoint - 48) | 0) >>> 0) <= 9) ? ((codePoint - 48) | 0) : (((((codePoint - 65) | 0) >>> 0) <= 25) ? ((codePoint - 55) | 0) : (((((codePoint - 97) | 0) >>> 0) <= 25) ? ((codePoint - 87) | 0) : (-1))));
  } else if (((((codePoint - 65313) | 0) >>> 0) <= 25)) {
    var value = ((codePoint - 65303) | 0);
  } else if (((((codePoint - 65345) | 0) >>> 0) <= 25)) {
    var value = ((codePoint - 65335) | 0);
  } else {
    var p = $m_ju_Arrays$().pk(this.i4, codePoint);
    var zeroCodePointIndex = ((p < 0) ? (((-2) - p) | 0) : p);
    if ((zeroCodePointIndex < 0)) {
      var value = (-1);
    } else {
      var v = ((codePoint - this.i4.a[zeroCodePointIndex]) | 0);
      var value = ((v > 9) ? (-1) : v);
    }
  }
  return ((value < radix) ? value : (-1));
});
var $d_jl_Character$ = new $TypeData().i($c_jl_Character$, "java.lang.Character$", ({
  ez: 1,
  a: 1
}));
var $n_jl_Character$;
function $m_jl_Character$() {
  if ((!$n_jl_Character$)) {
    $n_jl_Character$ = new $c_jl_Character$();
  }
  return $n_jl_Character$;
}
/** @constructor */
function $c_jl_Integer$() {
}
$p = $c_jl_Integer$.prototype = new $h_O();
$p.constructor = $c_jl_Integer$;
/** @constructor */
function $h_jl_Integer$() {
}
$h_jl_Integer$.prototype = $p;
$p.ga = (function(s) {
  throw new $c_jl_NumberFormatException((("For input string: \"" + s) + "\""));
});
$p.nJ = (function(s, radix, overflowBarrier) {
  if ((s === null)) {
    $m_jl_Integer$().ga(s);
  }
  var len = s.length;
  if ((len === 0)) {
    $m_jl_Integer$().ga(s);
  }
  var character = $m_jl_Character$();
  var firstChar = s.charCodeAt(0);
  var negative = (firstChar === 45);
  var sign = (negative ? (-1) : 0);
  var i = ((negative || (firstChar === 43)) | 0);
  if ((i >= len)) {
    $m_jl_Integer$().ga(s);
  }
  var java$lang$IntFloatBits$Int32Box$$value = 0;
  java$lang$IntFloatBits$Int32Box$$value = 0;
  while ((i !== len)) {
    var x = character.pJ(s.charCodeAt(i), radix);
    if (((x < 0) || ((java$lang$IntFloatBits$Int32Box$$value >>> 0) > (overflowBarrier >>> 0)))) {
      $m_jl_Integer$().ga(s);
    }
    var x$2 = java$lang$IntFloatBits$Int32Box$$value;
    var x$3 = Math.imul(x$2, radix);
    var v = ((x$3 + x) | 0);
    java$lang$IntFloatBits$Int32Box$$value = v;
    i = ((1 + i) | 0);
  }
  if (((java$lang$IntFloatBits$Int32Box$$value >>> 0) > (((2147483647 - sign) | 0) >>> 0))) {
    $m_jl_Integer$().ga(s);
  }
  return (((java$lang$IntFloatBits$Int32Box$$value ^ sign) - sign) | 0);
});
$p.dA = (function(i) {
  var t1 = ((i - (1431655765 & (i >> 1))) | 0);
  var t2 = (((858993459 & t1) + (858993459 & (t1 >> 2))) | 0);
  return (Math.imul(16843009, (252645135 & ((t2 + (t2 >> 4)) | 0))) >> 24);
});
var $d_jl_Integer$ = new $TypeData().i($c_jl_Integer$, "java.lang.Integer$", ({
  eF: 1,
  a: 1
}));
var $n_jl_Integer$;
function $m_jl_Integer$() {
  if ((!$n_jl_Integer$)) {
    $n_jl_Integer$ = new $c_jl_Integer$();
  }
  return $n_jl_Integer$;
}
/** @constructor */
function $c_jl_Number() {
}
$p = $c_jl_Number.prototype = new $h_O();
$p.constructor = $c_jl_Number;
/** @constructor */
function $h_jl_Number() {
}
$h_jl_Number.prototype = $p;
function $is_jl_Number(obj) {
  return (((obj instanceof $c_jl_Number) || ((typeof obj) === "number")) || (obj instanceof $Long));
}
function $isArrayOf_jl_Number(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.a8)));
}
/** @constructor */
function $c_jl_StackTraceElement(declaringClass, methodName, fileName, lineNumber, columnNumber) {
  this.es = null;
  this.fn = null;
  this.et = null;
  this.eu = 0;
  this.er = 0;
  this.es = declaringClass;
  this.fn = methodName;
  this.et = fileName;
  this.eu = lineNumber;
  this.er = columnNumber;
}
$p = $c_jl_StackTraceElement.prototype = new $h_O();
$p.constructor = $c_jl_StackTraceElement;
/** @constructor */
function $h_jl_StackTraceElement() {
}
$h_jl_StackTraceElement.prototype = $p;
$p.k = (function(that) {
  return ((that instanceof $c_jl_StackTraceElement) && (((((this.et === that.et) && (this.eu === that.eu)) && (this.er === that.er)) && (this.es === that.es)) && (this.fn === that.fn)));
});
$p.t = (function() {
  var result = "";
  if ((this.es !== "<jscode>")) {
    result = ((("" + result) + this.es) + ".");
  }
  result = (("" + result) + this.fn);
  if ((this.et === null)) {
    result = (result + "(Unknown Source)");
  } else {
    result = ((result + "(") + this.et);
    if ((this.eu >= 0)) {
      result = ((result + ":") + this.eu);
      if ((this.er >= 0)) {
        result = ((result + ":") + this.er);
      }
    }
    result = (result + ")");
  }
  return result;
});
$p.r = (function() {
  return (((($f_T__hashCode__I(this.es) ^ $f_T__hashCode__I(this.fn)) ^ $f_T__hashCode__I(this.et)) ^ this.eu) ^ this.er);
});
function $isArrayOf_jl_StackTraceElement(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.bA)));
}
var $d_jl_StackTraceElement = new $TypeData().i($c_jl_StackTraceElement, "java.lang.StackTraceElement", ({
  bA: 1,
  a: 1
}));
/** @constructor */
function $c_jl_String$() {
}
$p = $c_jl_String$.prototype = new $h_O();
$p.constructor = $c_jl_String$;
/** @constructor */
function $h_jl_String$() {
}
$h_jl_String$.prototype = $p;
$p.qE = (function(value, offset, count) {
  var endOffset = ((offset + count) | 0);
  var result = "";
  var i = offset;
  while ((i !== endOffset)) {
    result = (result + ("" + $cToS(value.a[i])));
    i = ((1 + i) | 0);
  }
  return result;
});
var $d_jl_String$ = new $TypeData().i($c_jl_String$, "java.lang.String$", ({
  eR: 1,
  a: 1
}));
var $n_jl_String$;
function $m_jl_String$() {
  if ((!$n_jl_String$)) {
    $n_jl_String$ = new $c_jl_String$();
  }
  return $n_jl_String$;
}
function $ct_jl_Throwable__T__jl_Throwable__Z__Z__($thiz, s, e, enableSuppression, writableStackTrace) {
  $thiz.lS = s;
  $thiz.fo = e;
  $thiz.lT = writableStackTrace;
  if (writableStackTrace) {
    $thiz.eP();
  }
  return $thiz;
}
class $c_jl_Throwable extends Error {
  constructor() {
    super();
    this.lS = null;
    this.fo = null;
    this.lT = false;
    this.lR = null;
    this.dP = null;
  }
  jc(cause) {
    this.fo = cause;
    return this;
  }
  eS() {
    return this.lS;
  }
  eP() {
    var reference = ((this instanceof $c_sjs_js_JavaScriptException) ? this.K : this);
    this.lR = ((Object.prototype.toString.call(reference) === "[object Error]") ? reference : (((Error.captureStackTrace === (void 0)) || (!(!Object.isSealed(this)))) ? new Error() : (Error.captureStackTrace(this), this)));
    return this;
  }
  h8() {
    if ((this.dP === null)) {
      if (this.lT) {
        this.dP = $m_jl_StackTrace$().pU(this.lR);
      } else {
        this.dP = new ($d_jl_StackTraceElement.r().C)(0);
      }
    }
    return this.dP;
  }
  gc(s) {
    this.h8();
    var t = this.t();
    s.e6(t);
    if ((this.dP.a.length !== 0)) {
      var i = 0;
      while ((i < this.dP.a.length)) {
        var t$1 = ("  at " + this.dP.a[i]);
        s.e6(t$1);
        i = ((1 + i) | 0);
      }
    } else {
      s.e6("  <no stack trace available>");
    }
    var wCause = this;
    while (((wCause !== wCause.fo) && (wCause.fo !== null))) {
      var parentTrace = wCause.h8();
      wCause = wCause.fo;
      var thisTrace = wCause.h8();
      var thisLength = thisTrace.a.length;
      var parentLength = parentTrace.a.length;
      var t$2 = ("Caused by: " + wCause);
      s.e6(t$2);
      if ((thisLength !== 0)) {
        var sameFrameCount = 0;
        while (true) {
          if (((sameFrameCount < thisLength) && (sameFrameCount < parentLength))) {
            var x = thisTrace.a[((((thisLength - sameFrameCount) | 0) - 1) | 0)];
            var x$2 = parentTrace.a[((((parentLength - sameFrameCount) | 0) - 1) | 0)];
            var $x_1 = ((x === null) ? (x$2 === null) : x.k(x$2));
          } else {
            var $x_1 = false;
          }
          if ($x_1) {
            sameFrameCount = ((1 + sameFrameCount) | 0);
          } else {
            break;
          }
        }
        if ((sameFrameCount > 0)) {
          sameFrameCount = ((sameFrameCount - 1) | 0);
        }
        var lengthToPrint = ((thisLength - sameFrameCount) | 0);
        var i$2 = 0;
        while ((i$2 < lengthToPrint)) {
          var t$3 = ("  at " + thisTrace.a[i$2]);
          s.e6(t$3);
          i$2 = ((1 + i$2) | 0);
        }
        if ((sameFrameCount > 0)) {
          var t$4 = (("  ... " + sameFrameCount) + " more");
          s.e6(t$4);
        }
      } else {
        s.e6("  <no stack trace available>");
      }
    }
  }
  t() {
    var className = $objectClassName(this);
    var message = this.eS();
    return ((message === null) ? className : ((className + ": ") + message));
  }
  r() {
    return $c_O.prototype.r.call(this);
  }
  k(that) {
    return $c_O.prototype.k.call(this, that);
  }
  get "message"() {
    var m = this.eS();
    return ((m === null) ? "" : m);
  }
  get "name"() {
    return $objectClassName(this);
  }
  "toString"() {
    return this.t();
  }
}
function $isArrayOf_jl_Throwable(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.s)));
}
function $ct_ju_concurrent_atomic_AtomicReference__O__($thiz, value) {
  $thiz.L = value;
  return $thiz;
}
/** @constructor */
function $c_ju_concurrent_atomic_AtomicReference() {
  this.L = null;
}
$p = $c_ju_concurrent_atomic_AtomicReference.prototype = new $h_O();
$p.constructor = $c_ju_concurrent_atomic_AtomicReference;
/** @constructor */
function $h_ju_concurrent_atomic_AtomicReference() {
}
$h_ju_concurrent_atomic_AtomicReference.prototype = $p;
$p.fY = (function(expect, update) {
  if (Object.is(expect, this.L)) {
    this.L = update;
    return true;
  } else {
    return false;
  }
});
$p.t = (function() {
  return ("" + this.L);
});
/** @constructor */
function $c_s_LowPriorityImplicits() {
}
$p = $c_s_LowPriorityImplicits.prototype = new $h_s_LowPriorityImplicits2();
$p.constructor = $c_s_LowPriorityImplicits;
/** @constructor */
function $h_s_LowPriorityImplicits() {
}
$h_s_LowPriorityImplicits.prototype = $p;
$p.rJ = (function(xs) {
  if ((xs === null)) {
    return null;
  } else if ((xs.a.length === 0)) {
    var this$2 = $m_scm_ArraySeq$();
    $m_s_reflect_ManifestFactory$ObjectManifest$();
    return this$2.mr;
  } else {
    return new $c_scm_ArraySeq$ofRef(xs);
  }
});
function $f_s_PartialFunction__applyOrElse__O__F1__O($thiz, x, default$1) {
  return ($thiz.ca(x) ? $thiz.b(x) : default$1.b(x));
}
/** @constructor */
function $c_sci_LazyList$Uninitialized$() {
}
$p = $c_sci_LazyList$Uninitialized$.prototype = new $h_O();
$p.constructor = $c_sci_LazyList$Uninitialized$;
/** @constructor */
function $h_sci_LazyList$Uninitialized$() {
}
$h_sci_LazyList$Uninitialized$.prototype = $p;
var $d_sci_LazyList$Uninitialized$ = new $TypeData().i($c_sci_LazyList$Uninitialized$, "scala.collection.immutable.LazyList$Uninitialized$", ({
  fZ: 1,
  a: 1
}));
var $n_sci_LazyList$Uninitialized$;
function $m_sci_LazyList$Uninitialized$() {
  if ((!$n_sci_LazyList$Uninitialized$)) {
    $n_sci_LazyList$Uninitialized$ = new $c_sci_LazyList$Uninitialized$();
  }
  return $n_sci_LazyList$Uninitialized$;
}
/** @constructor */
function $c_sci_MapNode() {
}
$p = $c_sci_MapNode.prototype = new $h_sci_Node();
$p.constructor = $c_sci_MapNode;
/** @constructor */
function $h_sci_MapNode() {
}
$h_sci_MapNode.prototype = $p;
function $f_scm_Growable__addAll__sc_IterableOnce__scm_Growable($thiz, elems) {
  if ((elems === $thiz)) {
    $thiz.aU($m_scm_Buffer$().nv(elems));
  } else {
    var it = elems.i();
    while (it.m()) {
      $thiz.aV(it.g());
    }
  }
  return $thiz;
}
function $f_s_concurrent_BatchingExecutor__submitSyncBatched__jl_Runnable__V($thiz, runnable) {
  var tl = $thiz.mB;
  var b = tl.s();
  if ((b instanceof $c_s_concurrent_BatchingExecutor$SyncBatch)) {
    b.qQ(runnable);
  } else {
    var i = ((b !== null) ? b : 0);
    if ((i < 16)) {
      tl.gf(((1 + i) | 0));
      try {
        runnable.e8();
      } catch (e) {
        var e$2 = ((e instanceof $c_jl_Throwable) ? e : new $c_sjs_js_JavaScriptException(e));
        if (false) {
          $m_s_concurrent_ExecutionContext$().eG.b(e$2);
        } else {
          matchResult3: {
            if ($m_s_util_control_NonFatal$().gW(e$2)) {
              $m_s_concurrent_ExecutionContext$().eG.b(e$2);
              break matchResult3;
            }
            throw ((e$2 instanceof $c_sjs_js_JavaScriptException) ? e$2.K : e$2);
          }
        }
      } finally {
        tl.gf(b);
      }
    } else {
      var batch = new $c_s_concurrent_BatchingExecutor$SyncBatch($thiz, runnable);
      tl.gf(batch);
      batch.e8();
      tl.gf(b);
    }
  }
}
/** @constructor */
function $c_s_concurrent_impl_Promise$ManyCallbacks(first, rest) {
  this.iA = null;
  this.iB = null;
  this.iA = first;
  this.iB = rest;
}
$p = $c_s_concurrent_impl_Promise$ManyCallbacks.prototype = new $h_O();
$p.constructor = $c_s_concurrent_impl_Promise$ManyCallbacks;
/** @constructor */
function $h_s_concurrent_impl_Promise$ManyCallbacks() {
}
$h_s_concurrent_impl_Promise$ManyCallbacks.prototype = $p;
$p.t = (function() {
  return "ManyCallbacks";
});
function $isArrayOf_s_concurrent_impl_Promise$ManyCallbacks(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.cv)));
}
var $d_s_concurrent_impl_Promise$ManyCallbacks = new $TypeData().i($c_s_concurrent_impl_Promise$ManyCallbacks, "scala.concurrent.impl.Promise$ManyCallbacks", ({
  cv: 1,
  av: 1
}));
/** @constructor */
function $c_sr_AbstractFunction0() {
}
$p = $c_sr_AbstractFunction0.prototype = new $h_O();
$p.constructor = $c_sr_AbstractFunction0;
/** @constructor */
function $h_sr_AbstractFunction0() {
}
$h_sr_AbstractFunction0.prototype = $p;
$p.t = (function() {
  return "<function0>";
});
/** @constructor */
function $c_sr_AbstractFunction1() {
}
$p = $c_sr_AbstractFunction1.prototype = new $h_O();
$p.constructor = $c_sr_AbstractFunction1;
/** @constructor */
function $h_sr_AbstractFunction1() {
}
$h_sr_AbstractFunction1.prototype = $p;
$p.t = (function() {
  return "<function1>";
});
/** @constructor */
function $c_sr_AbstractFunction2() {
}
$p = $c_sr_AbstractFunction2.prototype = new $h_O();
$p.constructor = $c_sr_AbstractFunction2;
/** @constructor */
function $h_sr_AbstractFunction2() {
}
$h_sr_AbstractFunction2.prototype = $p;
$p.t = (function() {
  return "<function2>";
});
/** @constructor */
function $c_sr_AbstractFunction3() {
}
$p = $c_sr_AbstractFunction3.prototype = new $h_O();
$p.constructor = $c_sr_AbstractFunction3;
/** @constructor */
function $h_sr_AbstractFunction3() {
}
$h_sr_AbstractFunction3.prototype = $p;
$p.t = (function() {
  return "<function3>";
});
/** @constructor */
function $c_sr_AbstractFunction4() {
}
$p = $c_sr_AbstractFunction4.prototype = new $h_O();
$p.constructor = $c_sr_AbstractFunction4;
/** @constructor */
function $h_sr_AbstractFunction4() {
}
$h_sr_AbstractFunction4.prototype = $p;
$p.t = (function() {
  return "<function4>";
});
/** @constructor */
function $c_sr_BooleanRef(elem) {
  this.gP = false;
  this.gP = elem;
}
$p = $c_sr_BooleanRef.prototype = new $h_O();
$p.constructor = $c_sr_BooleanRef;
/** @constructor */
function $h_sr_BooleanRef() {
}
$h_sr_BooleanRef.prototype = $p;
$p.t = (function() {
  return ("" + this.gP);
});
var $d_sr_BooleanRef = new $TypeData().i($c_sr_BooleanRef, "scala.runtime.BooleanRef", ({
  hK: 1,
  a: 1
}));
/** @constructor */
function $c_sr_IntRef(elem) {
  this.ab = 0;
  this.ab = elem;
}
$p = $c_sr_IntRef.prototype = new $h_O();
$p.constructor = $c_sr_IntRef;
/** @constructor */
function $h_sr_IntRef() {
}
$h_sr_IntRef.prototype = $p;
$p.t = (function() {
  return ("" + this.ab);
});
var $d_sr_IntRef = new $TypeData().i($c_sr_IntRef, "scala.runtime.IntRef", ({
  hM: 1,
  a: 1
}));
/** @constructor */
function $c_sr_ObjectRef(elem) {
  this.R = null;
  this.R = elem;
}
$p = $c_sr_ObjectRef.prototype = new $h_O();
$p.constructor = $c_sr_ObjectRef;
/** @constructor */
function $h_sr_ObjectRef() {
}
$h_sr_ObjectRef.prototype = $p;
$p.t = (function() {
  return ("" + this.R);
});
var $d_sr_ObjectRef = new $TypeData().i($c_sr_ObjectRef, "scala.runtime.ObjectRef", ({
  hQ: 1,
  a: 1
}));
/** @constructor */
function $c_s_util_hashing_MurmurHash3$() {
  this.ac = 0;
  this.dx = 0;
  this.mT = 0;
  this.iC = 0;
  $n_s_util_hashing_MurmurHash3$ = this;
  this.ac = $f_T__hashCode__I("Seq");
  this.dx = $f_T__hashCode__I("Map");
  this.mT = $f_T__hashCode__I("Set");
  this.iC = this.jv($m_sci_Nil$(), this.dx);
}
$p = $c_s_util_hashing_MurmurHash3$.prototype = new $h_s_util_hashing_MurmurHash3();
$p.constructor = $c_s_util_hashing_MurmurHash3$;
/** @constructor */
function $h_s_util_hashing_MurmurHash3$() {
}
$h_s_util_hashing_MurmurHash3$.prototype = $p;
$p.cc = (function(x, y) {
  return this.ok($m_sr_Statics$().C(x), $m_sr_Statics$().C(y), (-889275714));
});
$p.ob = (function(xs) {
  return ($is_sc_IndexedSeq(xs) ? this.ql(xs, this.ac) : ((xs instanceof $c_sci_List) ? this.qx(xs, this.ac) : this.qM(xs, this.ac)));
});
$p.qA = (function(xs) {
  if (xs.c()) {
    return this.iC;
  } else {
    var accum = new $c_s_util_hashing_MurmurHash3$accum$1();
    var h = this.dx;
    xs.e1(accum);
    h = this.w(h, accum.gR);
    h = this.w(h, accum.gS);
    h = this.cY(h, accum.gT);
    return this.ar(h, accum.gU);
  }
});
var $d_s_util_hashing_MurmurHash3$ = new $TypeData().i($c_s_util_hashing_MurmurHash3$, "scala.util.hashing.MurmurHash3$", ({
  iq: 1,
  ip: 1
}));
var $n_s_util_hashing_MurmurHash3$;
function $m_s_util_hashing_MurmurHash3$() {
  if ((!$n_s_util_hashing_MurmurHash3$)) {
    $n_s_util_hashing_MurmurHash3$ = new $c_s_util_hashing_MurmurHash3$();
  }
  return $n_s_util_hashing_MurmurHash3$;
}
/** @constructor */
function $c_s_util_hashing_MurmurHash3$accum$1() {
  this.gR = 0;
  this.gS = 0;
  this.gU = 0;
  this.gT = 0;
  this.gR = 0;
  this.gS = 0;
  this.gU = 0;
  this.gT = 1;
}
$p = $c_s_util_hashing_MurmurHash3$accum$1.prototype = new $h_O();
$p.constructor = $c_s_util_hashing_MurmurHash3$accum$1;
/** @constructor */
function $h_s_util_hashing_MurmurHash3$accum$1() {
}
$h_s_util_hashing_MurmurHash3$accum$1.prototype = $p;
$p.t = (function() {
  return "<function2>";
});
$p.pc = (function(k, v) {
  var h = $m_s_util_hashing_MurmurHash3$().cc(k, v);
  this.gR = ((this.gR + h) | 0);
  this.gS = (this.gS ^ h);
  this.gT = Math.imul(this.gT, (1 | h));
  this.gU = ((1 + this.gU) | 0);
});
$p.eM = (function(v1, v2) {
  this.pc(v1, v2);
});
var $d_s_util_hashing_MurmurHash3$accum$1 = new $TypeData().i($c_s_util_hashing_MurmurHash3$accum$1, "scala.util.hashing.MurmurHash3$accum$1", ({
  ir: 1,
  aI: 1
}));
class $c_Lcom_raquo_airstream_core_AirstreamError extends $c_jl_Throwable {
}
/** @constructor */
function $c_Lcom_raquo_airstream_core_AirstreamError$() {
  this.hp = null;
  this.jw = null;
  this.jx = null;
  $n_Lcom_raquo_airstream_core_AirstreamError$ = this;
  this.hp = $m_scm_Buffer$().nb($m_sr_ScalaRunTime$().b4(new ($d_F1.r().C)([])));
  this.jw = new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((err) => {
    try {
      console.error(((this.e2(err) + "\n") + this.qc(err, "\n")));
    } catch (e) {
      var e$2 = ((e instanceof $c_jl_Throwable) ? e : new $c_sjs_js_JavaScriptException(e));
      console.error("Error in AirstreamError.consoleErrorCallback:");
      console.error(e$2);
    }
  }));
  this.jx = new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((err$2) => {
    console.warn("Using unsafe rethrow error callback. Note: other registered error callbacks might not run. Use with caution.");
    var $x_1 = err$2;
    throw (($x_1 instanceof $c_sjs_js_JavaScriptException) ? $x_1.K : $x_1);
  }));
  this.qT(this.jw);
}
$p = $c_Lcom_raquo_airstream_core_AirstreamError$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_airstream_core_AirstreamError$;
/** @constructor */
function $h_Lcom_raquo_airstream_core_AirstreamError$() {
}
$h_Lcom_raquo_airstream_core_AirstreamError$.prototype = $p;
$p.e2 = (function(e) {
  try {
    var errorMessage = e.eS();
  } catch (e$2) {
    var errorMessage = "(Unable to get the message for this error - exception occurred in its getMessage)";
  }
  return (($objectGetClass(e).j8() + ": ") + errorMessage);
});
$p.qc = (function(err, newline) {
  try {
    return $f_sc_IterableOnceOps__mkString__T__T__T__T($m_s_Predef$().rJ(err.h8()), "", newline, "");
  } catch (e) {
    return "(Unable to get the stacktrace for this error - exception occurred in its getStackTrace)";
  }
});
$p.pu = (function(message, cause) {
  return ((message + "; cause: ") + (cause.c() ? $m_s_None$() : new $c_s_Some(this.e2(cause.s()))));
});
$p.qT = (function(fn) {
  this.hp.aV(fn);
});
$p.c2 = (function(err) {
  var this$1 = this.hp;
  var it = this$1.i();
  while (it.m()) {
    var x0 = it.g();
    try {
      x0.b(err);
    } catch (e) {
      var e$2 = ((e instanceof $c_jl_Throwable) ? e : new $c_sjs_js_JavaScriptException(e));
      var x$2 = this.jx;
      if (((x0 === null) ? (x$2 === null) : x0.k(x$2))) {
        throw ((e$2 instanceof $c_sjs_js_JavaScriptException) ? e$2.K : e$2);
      }
      console.warn("Error processing an unhandled error callback:");
      $m_sjs_js_timers_package$().rf(0.0, new $c_sjsr_AnonFunction0_$$Lambda$2bf0f8dc580d6edeb2d6a336c52a1bab3049702d(((e$2) => (() => {
        throw ((e$2 instanceof $c_sjs_js_JavaScriptException) ? e$2.K : e$2);
      }))(e$2)));
    }
  }
});
var $d_Lcom_raquo_airstream_core_AirstreamError$ = new $TypeData().i($c_Lcom_raquo_airstream_core_AirstreamError$, "com.raquo.airstream.core.AirstreamError$", ({
  cI: 1,
  he: 1,
  hf: 1
}));
var $n_Lcom_raquo_airstream_core_AirstreamError$;
function $m_Lcom_raquo_airstream_core_AirstreamError$() {
  if ((!$n_Lcom_raquo_airstream_core_AirstreamError$)) {
    $n_Lcom_raquo_airstream_core_AirstreamError$ = new $c_Lcom_raquo_airstream_core_AirstreamError$();
  }
  return $n_Lcom_raquo_airstream_core_AirstreamError$;
}
function $f_Lcom_raquo_airstream_core_BaseObservable__$init$__V($thiz) {
  $thiz.cu(true);
  $thiz.g7((void 0));
}
function $f_Lcom_raquo_airstream_core_BaseObservable__foreach__F1__Lcom_raquo_airstream_ownership_Owner__Lcom_raquo_airstream_ownership_Subscription($thiz, onNext, owner) {
  return $f_Lcom_raquo_airstream_core_WritableObservable__addObserver__Lcom_raquo_airstream_core_Observer__Lcom_raquo_airstream_ownership_Owner__Lcom_raquo_airstream_ownership_Subscription($thiz, $m_Lcom_raquo_airstream_core_Observer$().oq(onNext, $m_s_PartialFunction$().gC, true), owner);
}
function $f_Lcom_raquo_airstream_core_BaseObservable__removeExternalObserver__Lcom_raquo_airstream_core_Observer__V($thiz, observer) {
  if ($thiz.g5()) {
    $f_Lcom_raquo_airstream_core_WritableObservable__removeExternalObserverNow__Lcom_raquo_airstream_core_Observer__V($thiz, observer);
  } else {
    $f_Lcom_raquo_airstream_core_BaseObservable__getOrCreatePendingObserverRemovals__Lcom_raquo_ew_JsArray($thiz).push(new $c_sjsr_AnonFunction0_$$Lambda$2bf0f8dc580d6edeb2d6a336c52a1bab3049702d((() => {
      $f_Lcom_raquo_airstream_core_WritableObservable__removeExternalObserverNow__Lcom_raquo_airstream_core_Observer__V($thiz, observer);
    })));
  }
}
function $f_Lcom_raquo_airstream_core_BaseObservable__removeInternalObserver__Lcom_raquo_airstream_core_InternalObserver__V($thiz, observer) {
  if ($thiz.g5()) {
    $f_Lcom_raquo_airstream_core_WritableObservable__removeInternalObserverNow__Lcom_raquo_airstream_core_InternalObserver__V($thiz, observer);
  } else {
    $f_Lcom_raquo_airstream_core_BaseObservable__getOrCreatePendingObserverRemovals__Lcom_raquo_ew_JsArray($thiz).push(new $c_sjsr_AnonFunction0_$$Lambda$2bf0f8dc580d6edeb2d6a336c52a1bab3049702d((() => {
      $f_Lcom_raquo_airstream_core_WritableObservable__removeInternalObserverNow__Lcom_raquo_airstream_core_InternalObserver__V($thiz, observer);
    })));
  }
}
function $f_Lcom_raquo_airstream_core_BaseObservable__isStarted__Z($thiz) {
  return ($f_Lcom_raquo_airstream_core_WritableObservable__numAllObservers__I($thiz) > 0);
}
function $f_Lcom_raquo_airstream_core_BaseObservable__getOrCreatePendingObserverRemovals__Lcom_raquo_ew_JsArray($thiz) {
  var x = $thiz.e4();
  if ((x === (void 0))) {
    var newArray = $m_Lcom_raquo_ew_JsArray$().bb($m_sr_ScalaRunTime$().b4(new ($d_F0.r().C)([])));
    $thiz.g7(newArray);
    return newArray;
  } else {
    return x;
  }
}
var $d_Lcom_raquo_airstream_core_Observer = new $TypeData().i(1, "com.raquo.airstream.core.Observer", ({
  aA: 1,
  aq: 1,
  a5: 1
}));
function $f_Lcom_raquo_laminar_api_Implicits__textToTextNode__O__Lcom_raquo_laminar_modifiers_RenderableText__Lcom_raquo_laminar_nodes_TextNode($thiz, value, r) {
  return new $c_Lcom_raquo_laminar_nodes_TextNode(r.iK(value));
}
function $f_Lcom_raquo_laminar_api_Implicits__nodeSeqToModifier__O__Lcom_raquo_laminar_modifiers_RenderableSeq__Lcom_raquo_laminar_modifiers_Modifier($thiz, nodes, renderableSeq) {
  return new $c_Lcom_raquo_laminar_modifiers_Modifier$$anon$2(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((element) => {
    ($m_Lcom_raquo_laminar_Seq$(), new $c_Lcom_raquo_laminar_Seq(nodes, null, null)).bm(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((element$2) => ((_$9) => {
      $m_Lcom_raquo_laminar_nodes_ParentNode$().eL(element$2, _$9, (void 0));
    }))(element)));
  })), $m_Lcom_raquo_laminar_modifiers_Modifier$());
}
/** @constructor */
function $c_Lcom_raquo_laminar_api_Laminar$$anon$1() {
  this.kq = null;
  this.kr = false;
}
$p = $c_Lcom_raquo_laminar_api_Laminar$$anon$1.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_api_Laminar$$anon$1;
/** @constructor */
function $h_Lcom_raquo_laminar_api_Laminar$$anon$1() {
}
$h_Lcom_raquo_laminar_api_Laminar$$anon$1.prototype = $p;
$p.qK = (function() {
  if ((!this.kr)) {
    this.kq = new $c_Lcom_raquo_laminar_keys_EventProp("DOMContentLoaded");
    this.kr = true;
  }
  return this.kq;
});
var $d_Lcom_raquo_laminar_api_Laminar$$anon$1 = new $TypeData().i($c_Lcom_raquo_laminar_api_Laminar$$anon$1, "com.raquo.laminar.api.Laminar$$anon$1", ({
  dk: 1,
  bf: 1,
  dy: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_modifiers_CompositeKeySetter(key, itemsToAdd) {
  this.lz = null;
  this.hR = null;
  this.lz = key;
  this.hR = itemsToAdd;
}
$p = $c_Lcom_raquo_laminar_modifiers_CompositeKeySetter.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_modifiers_CompositeKeySetter;
/** @constructor */
function $h_Lcom_raquo_laminar_modifiers_CompositeKeySetter() {
}
$h_Lcom_raquo_laminar_modifiers_CompositeKeySetter.prototype = $p;
$p.co = (function(element) {
  if ((!this.hR.c())) {
    $f_Lcom_raquo_laminar_nodes_ReactiveElement__updateCompositeValue__Lcom_raquo_laminar_keys_CompositeKey__Lcom_raquo_laminar_modifiers_Modifier__sci_List__sci_List__V(element, this.lz, null, this.hR, $m_sci_Nil$());
  }
});
var $d_Lcom_raquo_laminar_modifiers_CompositeKeySetter = new $TypeData().i($c_Lcom_raquo_laminar_modifiers_CompositeKeySetter, "com.raquo.laminar.modifiers.CompositeKeySetter", ({
  dY: 1,
  X: 1,
  bj: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_modifiers_EventListener(eventProcessor, callback) {
  this.ej = null;
  this.hS = null;
  this.hT = null;
  this.ej = eventProcessor;
  this.hS = ((ev) => {
    var processor = eventProcessor.gv;
    var this$2 = processor.b(ev);
    if ((!this$2.c())) {
      callback.b(this$2.s());
    }
  });
  this.hT = (() => {
    var outer = null;
    outer = this;
    var this$3 = ({});
    if ((outer === null)) {
      throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
    }
    this$3.capture = outer.ej.gw;
    this$3.passive = outer.ej.hL;
    return this$3;
  })();
}
$p = $c_Lcom_raquo_laminar_modifiers_EventListener.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_modifiers_EventListener;
/** @constructor */
function $h_Lcom_raquo_laminar_modifiers_EventListener() {
}
$h_Lcom_raquo_laminar_modifiers_EventListener.prototype = $p;
$p.co = (function(element) {
  this.pl(element, false);
});
$p.pl = (function(element, unsafePrepend) {
  if (($f_Lcom_raquo_laminar_nodes_ReactiveElement__indexOfEventListener__Lcom_raquo_laminar_modifiers_EventListener__I(element, this) === (-1))) {
    var subscribe = new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((ctx) => {
      $m_Lcom_raquo_laminar_DomApi$().oW(element.b5, this);
      return new $c_Lcom_raquo_airstream_ownership_Subscription(ctx.hQ, new $c_sjsr_AnonFunction0_$$Lambda$2bf0f8dc580d6edeb2d6a336c52a1bab3049702d((() => {
        var listenerIndex = $f_Lcom_raquo_laminar_nodes_ReactiveElement__indexOfEventListener__Lcom_raquo_laminar_modifiers_EventListener__I(element, this);
        if ((listenerIndex !== (-1))) {
          $f_Lcom_raquo_laminar_nodes_ReactiveElement__removeEventListener__I__V(element, listenerIndex);
          $m_Lcom_raquo_laminar_DomApi$().qX(element.b5, this);
        }
      })));
    }));
    var sub = (unsafePrepend ? $m_Lcom_raquo_laminar_nodes_ReactiveElement$().rE(element, subscribe) : $m_Lcom_raquo_airstream_ownership_DynamicSubscription$().gk(element.c4, new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((owner) => subscribe.b(new $c_Lcom_raquo_laminar_lifecycle_MountContext(element, owner)))), false));
    $f_Lcom_raquo_laminar_nodes_ReactiveElement__addEventListener__Lcom_raquo_laminar_modifiers_EventListener__Z__V(element, this, unsafePrepend);
    return sub;
  } else {
    var activate = new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((_$1) => (void 0)));
    return $m_Lcom_raquo_airstream_ownership_DynamicSubscription$().og(element.c4, new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((owner$1) => {
      activate.b(new $c_Lcom_raquo_laminar_lifecycle_MountContext(element, owner$1));
    })), false);
  }
});
$p.t = (function() {
  return (("EventListener(" + this.ej.ei.f9) + ")");
});
var $d_Lcom_raquo_laminar_modifiers_EventListener = new $TypeData().i($c_Lcom_raquo_laminar_modifiers_EventListener, "com.raquo.laminar.modifiers.EventListener", ({
  dZ: 1,
  X: 1,
  bi: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_modifiers_KeySetter(key, value, action) {
  this.lB = null;
  this.lC = null;
  this.lA = null;
  this.lB = key;
  this.lC = value;
  this.lA = action;
}
$p = $c_Lcom_raquo_laminar_modifiers_KeySetter.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_modifiers_KeySetter;
/** @constructor */
function $h_Lcom_raquo_laminar_modifiers_KeySetter() {
}
$h_Lcom_raquo_laminar_modifiers_KeySetter.prototype = $p;
$p.co = (function(element) {
  this.lA.iI(element, this.lB, this.lC);
});
var $d_Lcom_raquo_laminar_modifiers_KeySetter = new $TypeData().i($c_Lcom_raquo_laminar_modifiers_KeySetter, "com.raquo.laminar.modifiers.KeySetter", ({
  e0: 1,
  X: 1,
  bj: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_modifiers_KeyUpdater(key, values, update) {
  this.lD = null;
  this.lF = null;
  this.lE = null;
  this.lD = key;
  this.lF = values;
  this.lE = update;
}
$p = $c_Lcom_raquo_laminar_modifiers_KeyUpdater.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_modifiers_KeyUpdater;
/** @constructor */
function $h_Lcom_raquo_laminar_modifiers_KeyUpdater() {
}
$h_Lcom_raquo_laminar_modifiers_KeyUpdater.prototype = $p;
$p.co = (function(element) {
  this.iL(element);
});
$p.iL = (function(element) {
  element.qJ(this.lD);
  var observable = this.lF;
  var onNext = new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((value) => {
    this.lE.iI(element, value, this);
  }));
  return $m_Lcom_raquo_airstream_ownership_DynamicSubscription$().rh(element.c4, observable, onNext);
});
var $d_Lcom_raquo_laminar_modifiers_KeyUpdater = new $TypeData().i($c_Lcom_raquo_laminar_modifiers_KeyUpdater, "com.raquo.laminar.modifiers.KeyUpdater", ({
  e1: 1,
  X: 1,
  bi: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_nodes_RootNode(container, child) {
  this.i0 = null;
  this.lJ = null;
  this.lK = null;
  this.lJ = child;
  $f_Lcom_raquo_laminar_nodes_ParentNode__$init$__V(this);
  if ((container === null)) {
    throw $ct_jl_Exception__T__(new $c_jl_Exception(), "Unable to mount Laminar RootNode into a null container. See https://laminar.dev/documentation#waiting-for-the-dom-to-load");
  }
  if ((!$m_Lcom_raquo_laminar_DomApi$().qw(container, document))) {
    throw $ct_jl_Exception__T__(new $c_jl_Exception(), "Unable to mount Laminar RootNode into an unmounted container. See https://laminar.dev/documentation#rendering");
  }
  this.lK = container;
  this.qC();
}
$p = $c_Lcom_raquo_laminar_nodes_RootNode.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_nodes_RootNode;
/** @constructor */
function $h_Lcom_raquo_laminar_nodes_RootNode() {
}
$h_Lcom_raquo_laminar_nodes_RootNode.prototype = $p;
$p.h3 = (function() {
  return this.i0;
});
$p.ng = (function(x$0) {
  this.i0 = x$0;
});
$p.qC = (function() {
  this.i0.mX();
  return $m_Lcom_raquo_laminar_nodes_ParentNode$().eL(this, this.lJ, (void 0));
});
$p.I = (function() {
  return this.lK;
});
var $d_Lcom_raquo_laminar_nodes_RootNode = new $TypeData().i($c_Lcom_raquo_laminar_nodes_RootNode, "com.raquo.laminar.nodes.RootNode", ({
  ei: 1,
  as: 1,
  bk: 1
}));
function $isArrayOf_Lcom_raquo_laminar_tags_CustomHtmlTag(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.en)));
}
function $p_jl_Class__computeCachedSimpleNameBestEffort__T($thiz) {
  if ($thiz.ah.Z) {
    return ($thiz.ah.Q().j8() + "[]");
  } else {
    var name = $thiz.ah.N;
    var idx = ((name.length - 1) | 0);
    while (((idx >= 0) && (name.charCodeAt(idx) === 36))) {
      idx = ((idx - 1) | 0);
    }
    if (((idx >= 0) && ((((name.charCodeAt(idx) - 48) | 0) >>> 0) <= 9))) {
      idx = ((idx - 1) | 0);
      while (((idx >= 0) && ((((name.charCodeAt(idx) - 48) | 0) >>> 0) <= 9))) {
        idx = ((idx - 1) | 0);
      }
      while (((idx >= 0) && (name.charCodeAt(idx) === 36))) {
        idx = ((idx - 1) | 0);
      }
    }
    while (true) {
      if ((idx >= 0)) {
        var index$4 = idx;
        var currChar = name.charCodeAt(index$4);
        var $x_1 = ((currChar !== 36) && (currChar !== 46));
      } else {
        var $x_1 = false;
      }
      if ($x_1) {
        idx = ((idx - 1) | 0);
      } else {
        break;
      }
    }
    var beginIndex = ((1 + idx) | 0);
    return name.substring(beginIndex);
  }
}
/** @constructor */
function $c_jl_Class($data) {
  this.i5 = null;
  this.ah = $data;
}
$p = $c_jl_Class.prototype = new $h_O();
$p.constructor = $c_jl_Class;
/** @constructor */
function $h_jl_Class() {
}
$h_jl_Class.prototype = $p;
$p.t = (function() {
  return ((this.ah.Y ? "interface " : (this.ah.X ? "" : "class ")) + this.ah.N);
});
$p.j8 = (function() {
  if ((this.i5 === null)) {
    this.i5 = $p_jl_Class__computeCachedSimpleNameBestEffort__T(this);
  }
  return this.i5;
});
var $d_jl_Class = new $TypeData().i($c_jl_Class, "java.lang.Class", ({
  eA: 1,
  a: 1,
  Y: 1
}));
class $c_jl_Error extends $c_jl_Throwable {
}
function $isArrayOf_jl_Error(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.bw)));
}
function $ct_jl_Exception__T__($thiz, s) {
  $ct_jl_Throwable__T__jl_Throwable__Z__Z__($thiz, s, null, true, true);
  return $thiz;
}
class $c_jl_Exception extends $c_jl_Throwable {
}
var $d_jl_Exception = new $TypeData().i($c_jl_Exception, "java.lang.Exception", ({
  B: 1,
  s: 1,
  a: 1
}));
/** @constructor */
function $c_s_Predef$() {
  this.oB = null;
  $n_s_Predef$ = this;
  $m_sci_List$();
  this.oB = $m_sci_Map$();
}
$p = $c_s_Predef$.prototype = new $h_s_LowPriorityImplicits();
$p.constructor = $c_s_Predef$;
/** @constructor */
function $h_s_Predef$() {
}
$h_s_Predef$.prototype = $p;
$p.r2 = (function(requirement) {
  if ((!requirement)) {
    throw $ct_jl_IllegalArgumentException__T__(new $c_jl_IllegalArgumentException(), "requirement failed");
  }
});
var $d_s_Predef$ = new $TypeData().i($c_s_Predef$, "scala.Predef$", ({
  ff: 1,
  f8: 1,
  f9: 1
}));
var $n_s_Predef$;
function $m_s_Predef$() {
  if ((!$n_s_Predef$)) {
    $n_s_Predef$ = new $c_s_Predef$();
  }
  return $n_s_Predef$;
}
function $f_s_Product2__productElement__I__O($thiz, n) {
  switch (n) {
    case 0: {
      return $thiz.aZ;
      break;
    }
    case 1: {
      return $thiz.aQ;
      break;
    }
    default: {
      throw $ct_jl_IndexOutOfBoundsException__T__(new $c_jl_IndexOutOfBoundsException(), (n + " is out of bounds (min 0, max 1)"));
    }
  }
}
function $ct_sc_ClassTagIterableFactory$AnyIterableDelegate__sc_ClassTagIterableFactory__($thiz, delegate) {
  $thiz.fr = delegate;
  return $thiz;
}
/** @constructor */
function $c_sc_ClassTagIterableFactory$AnyIterableDelegate() {
  this.fr = null;
}
$p = $c_sc_ClassTagIterableFactory$AnyIterableDelegate.prototype = new $h_O();
$p.constructor = $c_sc_ClassTagIterableFactory$AnyIterableDelegate;
/** @constructor */
function $h_sc_ClassTagIterableFactory$AnyIterableDelegate() {
}
$h_sc_ClassTagIterableFactory$AnyIterableDelegate.prototype = $p;
$p.ag = (function(it) {
  return this.fr.j0(it, $m_s_reflect_ManifestFactory$AnyManifest$());
});
$p.aW = (function() {
  return this.fr.hc($m_s_reflect_ManifestFactory$AnyManifest$());
});
$p.cT = (function(elems) {
  return this.fr.j0(elems, $m_s_reflect_ManifestFactory$AnyManifest$());
});
function $ct_sc_IterableFactory$Delegate__sc_IterableFactory__($thiz, delegate) {
  $thiz.gE = delegate;
  return $thiz;
}
/** @constructor */
function $c_sc_IterableFactory$Delegate() {
  this.gE = null;
}
$p = $c_sc_IterableFactory$Delegate.prototype = new $h_O();
$p.constructor = $c_sc_IterableFactory$Delegate;
/** @constructor */
function $h_sc_IterableFactory$Delegate() {
}
$h_sc_IterableFactory$Delegate.prototype = $p;
$p.ag = (function(it) {
  return this.gE.ag(it);
});
$p.aW = (function() {
  return this.gE.aW();
});
function $f_sc_IterableOps__sizeCompare__I__I($thiz, otherSize) {
  if ((otherSize < 0)) {
    return 1;
  } else {
    var known = $thiz.x();
    if ((known >= 0)) {
      return ((known === otherSize) ? 0 : ((known < otherSize) ? (-1) : 1));
    } else {
      var i = 0;
      var it = $thiz.i();
      while (it.m()) {
        if ((i === otherSize)) {
          return 1;
        }
        it.g();
        i = ((1 + i) | 0);
      }
      return ((i - otherSize) | 0);
    }
  }
}
function $f_sc_Iterator__concat__F0__sc_Iterator($thiz, xs) {
  return new $c_sc_Iterator$ConcatIterator($thiz).iO(xs);
}
function $f_sc_Iterator__sliceIterator__I__I__sc_Iterator($thiz, from, until) {
  var lo = ((from > 0) ? from : 0);
  var rest = ((until < 0) ? (-1) : ((until <= lo) ? 0 : ((until - lo) | 0)));
  return ((rest === 0) ? $m_sc_Iterator$().O : new $c_sc_Iterator$SliceIterator($thiz, lo, rest));
}
function $f_sc_Iterator__sameElements__sc_IterableOnce__Z($thiz, that) {
  var those = that.i();
  while ($thiz.m()) {
    if ((!those.m())) {
      return false;
    }
    if ((!$m_sr_BoxesRunTime$().j($thiz.g(), those.g()))) {
      return false;
    }
  }
  return (!those.m());
}
/** @constructor */
function $c_sc_Iterator$() {
  this.O = null;
  $n_sc_Iterator$ = this;
  this.O = new $c_sc_Iterator$$anon$19();
}
$p = $c_sc_Iterator$.prototype = new $h_O();
$p.constructor = $c_sc_Iterator$;
/** @constructor */
function $h_sc_Iterator$() {
}
$h_sc_Iterator$.prototype = $p;
$p.aW = (function() {
  return new $c_sc_Iterator$$anon$21();
});
$p.ag = (function(source) {
  return source.i();
});
var $d_sc_Iterator$ = new $TypeData().i($c_sc_Iterator$, "scala.collection.Iterator$", ({
  fr: 1,
  a: 1,
  K: 1
}));
var $n_sc_Iterator$;
function $m_sc_Iterator$() {
  if ((!$n_sc_Iterator$)) {
    $n_sc_Iterator$ = new $c_sc_Iterator$();
  }
  return $n_sc_Iterator$;
}
function $ct_sc_MapFactory$Delegate__sc_MapFactory__($thiz, delegate) {
  $thiz.ig = delegate;
  return $thiz;
}
/** @constructor */
function $c_sc_MapFactory$Delegate() {
  this.ig = null;
}
$p = $c_sc_MapFactory$Delegate.prototype = new $h_O();
$p.constructor = $c_sc_MapFactory$Delegate;
/** @constructor */
function $h_sc_MapFactory$Delegate() {
}
$h_sc_MapFactory$Delegate.prototype = $p;
$p.ag = (function(it) {
  return this.ig.ag(it);
});
/** @constructor */
function $c_sc_View$() {
}
$p = $c_sc_View$.prototype = new $h_O();
$p.constructor = $c_sc_View$;
/** @constructor */
function $h_sc_View$() {
}
$h_sc_View$.prototype = $p;
$p.nw = (function(it) {
  return ($is_sc_View(it) ? it : ($is_sc_Iterable(it) ? new $c_sc_View$$anon$1(new $c_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c(((it$2) => (() => it$2.i()))(it))) : $ct_sc_SeqView$Id__sc_SeqOps__(new $c_sc_SeqView$Id(), $m_sci_LazyList$().j2(it))));
});
$p.aW = (function() {
  return new $c_scm_Builder$$anon$1(new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((it$2) => this.nw(it$2))), ($m_scm_ArrayBuffer$(), new $c_scm_ArrayBuffer$$anon$1()));
});
$p.ag = (function(source) {
  return this.nw(source);
});
var $d_sc_View$ = new $TypeData().i($c_sc_View$, "scala.collection.View$", ({
  fG: 1,
  a: 1,
  K: 1
}));
var $n_sc_View$;
function $m_sc_View$() {
  if ((!$n_sc_View$)) {
    $n_sc_View$ = new $c_sc_View$();
  }
  return $n_sc_View$;
}
/** @constructor */
function $c_sci_BitmapIndexedMapNode(dataMap, nodeMap, content, originalHashes, size, cachedJavaKeySetHashCode) {
  this.N = 0;
  this.T = 0;
  this.ae = null;
  this.bt = null;
  this.aE = 0;
  this.bd = 0;
  this.N = dataMap;
  this.T = nodeMap;
  this.ae = content;
  this.bt = originalHashes;
  this.aE = size;
  this.bd = cachedJavaKeySetHashCode;
}
$p = $c_sci_BitmapIndexedMapNode.prototype = new $h_sci_MapNode();
$p.constructor = $c_sci_BitmapIndexedMapNode;
/** @constructor */
function $h_sci_BitmapIndexedMapNode() {
}
$h_sci_BitmapIndexedMapNode.prototype = $p;
$p.ax = (function() {
  return this.aE;
});
$p.dB = (function() {
  return this.bd;
});
$p.cW = (function(index) {
  return this.ae.a[(index << 1)];
});
$p.ct = (function(index) {
  return this.ae.a[((1 + (index << 1)) | 0)];
});
$p.nD = (function(index) {
  return new $c_T2(this.ae.a[(index << 1)], this.ae.a[((1 + (index << 1)) | 0)]);
});
$p.g3 = (function(index) {
  return this.bt.a[index];
});
$p.cs = (function(index) {
  return this.ae.a[((((this.ae.a.length - 1) | 0) - index) | 0)];
});
$p.iH = (function(key, originalHash, keyHash, shift) {
  var mask = $m_sci_Node$().dE(keyHash, shift);
  var bitpos = $m_sci_Node$().cU(mask);
  if (((this.N & bitpos) !== 0)) {
    var index = $m_sci_Node$().c1(this.N, mask, bitpos);
    if ($m_sr_BoxesRunTime$().j(key, this.cW(index))) {
      return this.ct(index);
    } else {
      throw $ct_ju_NoSuchElementException__T__(new $c_ju_NoSuchElementException(), ("key not found: " + key));
    }
  } else if (((this.T & bitpos) !== 0)) {
    return this.cs($m_sci_Node$().c1(this.T, mask, bitpos)).iH(key, originalHash, keyHash, ((5 + shift) | 0));
  } else {
    throw $ct_ju_NoSuchElementException__T__(new $c_ju_NoSuchElementException(), ("key not found: " + key));
  }
});
$p.h7 = (function(key, originalHash, keyHash, shift) {
  var mask = $m_sci_Node$().dE(keyHash, shift);
  var bitpos = $m_sci_Node$().cU(mask);
  if (((this.N & bitpos) !== 0)) {
    var index = $m_sci_Node$().c1(this.N, mask, bitpos);
    return ($m_sr_BoxesRunTime$().j(key, this.cW(index)) ? new $c_s_Some(this.ct(index)) : $m_s_None$());
  } else {
    return (((this.T & bitpos) !== 0) ? this.cs($m_sci_Node$().c1(this.T, mask, bitpos)).h7(key, originalHash, keyHash, ((5 + shift) | 0)) : $m_s_None$());
  }
});
$p.j6 = (function(key, originalHash, keyHash, shift, f) {
  var mask = $m_sci_Node$().dE(keyHash, shift);
  var bitpos = $m_sci_Node$().cU(mask);
  if (((this.N & bitpos) !== 0)) {
    var index = $m_sci_Node$().c1(this.N, mask, bitpos);
    return ($m_sr_BoxesRunTime$().j(key, this.cW(index)) ? this.ct(index) : f.F());
  } else {
    return (((this.T & bitpos) !== 0) ? this.cs($m_sci_Node$().c1(this.T, mask, bitpos)).j6(key, originalHash, keyHash, ((5 + shift) | 0), f) : f.F());
  }
});
$p.iP = (function(key, originalHash, keyHash, shift) {
  var mask = $m_sci_Node$().dE(keyHash, shift);
  var bitpos = $m_sci_Node$().cU(mask);
  if (((this.N & bitpos) !== 0)) {
    var index = $m_sci_Node$().c1(this.N, mask, bitpos);
    return ((this.bt.a[index] === originalHash) && $m_sr_BoxesRunTime$().j(key, this.cW(index)));
  } else {
    return (((this.T & bitpos) !== 0) && this.cs($m_sci_Node$().c1(this.T, mask, bitpos)).iP(key, originalHash, keyHash, ((5 + shift) | 0)));
  }
});
$p.om = (function(key, value, originalHash, keyHash, shift, replaceValue) {
  var mask = $m_sci_Node$().dE(keyHash, shift);
  var bitpos = $m_sci_Node$().cU(mask);
  if (((this.N & bitpos) !== 0)) {
    var index = $m_sci_Node$().c1(this.N, mask, bitpos);
    var key0 = this.cW(index);
    var key0UnimprovedHash = this.g3(index);
    if (((key0UnimprovedHash === originalHash) && $m_sr_BoxesRunTime$().j(key0, key))) {
      if (replaceValue) {
        var value0 = this.ct(index);
        return ((Object.is(key0, key) && Object.is(value0, value)) ? this : this.pA(bitpos, key, value));
      } else {
        return this;
      }
    } else {
      var value0$2 = this.ct(index);
      var key0Hash = $m_sc_Hashing$().c0(key0UnimprovedHash);
      return this.py(bitpos, key0Hash, this.ji(key0, value0$2, key0UnimprovedHash, key0Hash, key, value, originalHash, keyHash, ((5 + shift) | 0)));
    }
  } else if (((this.T & bitpos) !== 0)) {
    var index$2 = $m_sci_Node$().c1(this.T, mask, bitpos);
    var subNode = this.cs(index$2);
    var subNodeNew$2 = subNode.on(key, value, originalHash, keyHash, ((5 + shift) | 0), replaceValue);
    return ((subNodeNew$2 === subNode) ? this : this.pz(bitpos, subNode, subNodeNew$2));
  } else {
    return this.px(bitpos, key, originalHash, keyHash, value);
  }
});
$p.ji = (function(key0, value0, originalHash0, keyHash0, key1, value1, originalHash1, keyHash1, shift) {
  if ((shift >= 32)) {
    return new $c_sci_HashCollisionMapNode(originalHash0, keyHash0, $m_sci_Vector$().j3(new $c_sjsr_WrappedVarArgs([new $c_T2(key0, value0), new $c_T2(key1, value1)])));
  } else {
    var mask0 = $m_sci_Node$().dE(keyHash0, shift);
    var mask1 = $m_sci_Node$().dE(keyHash1, shift);
    var newCachedHash = ((keyHash0 + keyHash1) | 0);
    if ((mask0 !== mask1)) {
      var dataMap = ($m_sci_Node$().cU(mask0) | $m_sci_Node$().cU(mask1));
      if ((mask0 < mask1)) {
        var xs = new $c_sjsr_WrappedVarArgs([key0, value0, key1, value1]);
        var array$2 = new $ac_O(xs.q());
        var iterator = $ct_sc_IndexedSeqView$IndexedSeqViewIterator__sc_IndexedSeqView__(new $c_sc_IndexedSeqView$IndexedSeqViewIterator(), new $c_sc_IndexedSeqView$Id(xs));
        var i = 0;
        while ((iterator.b6 > 0)) {
          array$2.a[i] = iterator.g();
          i = ((1 + i) | 0);
        }
        return new $c_sci_BitmapIndexedMapNode(dataMap, 0, array$2, new $ac_I(new Int32Array([originalHash0, originalHash1])), 2, newCachedHash);
      } else {
        var xs$1 = new $c_sjsr_WrappedVarArgs([key1, value1, key0, value0]);
        var array$4 = new $ac_O(xs$1.q());
        var iterator$1 = $ct_sc_IndexedSeqView$IndexedSeqViewIterator__sc_IndexedSeqView__(new $c_sc_IndexedSeqView$IndexedSeqViewIterator(), new $c_sc_IndexedSeqView$Id(xs$1));
        var i$1 = 0;
        while ((iterator$1.b6 > 0)) {
          array$4.a[i$1] = iterator$1.g();
          i$1 = ((1 + i$1) | 0);
        }
        return new $c_sci_BitmapIndexedMapNode(dataMap, 0, array$4, new $ac_I(new Int32Array([originalHash1, originalHash0])), 2, newCachedHash);
      }
    } else {
      var nodeMap = $m_sci_Node$().cU(mask0);
      var node = this.ji(key0, value0, originalHash0, keyHash0, key1, value1, originalHash1, keyHash1, ((5 + shift) | 0));
      var xs$2 = new $c_sjsr_WrappedVarArgs([node]);
      var array$6 = new $ac_O(xs$2.q());
      var iterator$2 = $ct_sc_IndexedSeqView$IndexedSeqViewIterator__sc_IndexedSeqView__(new $c_sc_IndexedSeqView$IndexedSeqViewIterator(), new $c_sc_IndexedSeqView$Id(xs$2));
      var i$2 = 0;
      while ((iterator$2.b6 > 0)) {
        array$6.a[i$2] = iterator$2.g();
        i$2 = ((1 + i$2) | 0);
      }
      return new $c_sci_BitmapIndexedMapNode(0, nodeMap, array$6, $m_s_Array$EmptyArrays$().ic, node.ax(), node.dB());
    }
  }
});
$p.j9 = (function() {
  return (this.T !== 0);
});
$p.jj = (function() {
  return $m_jl_Integer$().dA(this.T);
});
$p.h9 = (function() {
  return (this.N !== 0);
});
$p.jo = (function() {
  return $m_jl_Integer$().dA(this.N);
});
$p.g0 = (function(bitpos) {
  return $m_jl_Integer$().dA((this.N & ((bitpos - 1) | 0)));
});
$p.jk = (function(bitpos) {
  return $m_jl_Integer$().dA((this.T & ((bitpos - 1) | 0)));
});
$p.pA = (function(bitpos, newKey, newValue) {
  var dataIx = this.g0(bitpos);
  var idx = (dataIx << 1);
  var src = this.ae;
  var dst = new $ac_O(src.a.length);
  var length = src.a.length;
  src.u(0, dst, 0, length);
  dst.a[((1 + idx) | 0)] = newValue;
  return new $c_sci_BitmapIndexedMapNode(this.N, this.T, dst, this.bt, this.aE, this.bd);
});
$p.pz = (function(bitpos, oldNode, newNode) {
  var idx = ((((this.ae.a.length - 1) | 0) - this.jk(bitpos)) | 0);
  var src = this.ae;
  var dst = new $ac_O(src.a.length);
  var length = src.a.length;
  src.u(0, dst, 0, length);
  dst.a[idx] = newNode;
  return new $c_sci_BitmapIndexedMapNode(this.N, this.T, dst, this.bt, ((((this.aE - oldNode.ax()) | 0) + newNode.ax()) | 0), ((((this.bd - oldNode.dB()) | 0) + newNode.dB()) | 0));
});
$p.px = (function(bitpos, key, originalHash, keyHash, value) {
  var dataIx = this.g0(bitpos);
  var idx = (dataIx << 1);
  var src = this.ae;
  var dst = new $ac_O(((2 + src.a.length) | 0));
  src.u(0, dst, 0, idx);
  dst.a[idx] = key;
  dst.a[((1 + idx) | 0)] = value;
  var destPos = ((2 + idx) | 0);
  var length = ((src.a.length - idx) | 0);
  src.u(idx, dst, destPos, length);
  var dstHashes = this.qq(this.bt, dataIx, originalHash);
  return new $c_sci_BitmapIndexedMapNode((this.N | bitpos), this.T, dst, dstHashes, ((1 + this.aE) | 0), ((this.bd + keyHash) | 0));
});
$p.qB = (function(bitpos, keyHash, node) {
  var dataIx = this.g0(bitpos);
  var idxOld = (dataIx << 1);
  var idxNew = ((((this.ae.a.length - 2) | 0) - this.jk(bitpos)) | 0);
  var src = this.ae;
  var dst = new $ac_O(((src.a.length - 1) | 0));
  src.u(0, dst, 0, idxOld);
  var srcPos = ((2 + idxOld) | 0);
  var length = ((idxNew - idxOld) | 0);
  src.u(srcPos, dst, idxOld, length);
  dst.a[idxNew] = node;
  var srcPos$1 = ((2 + idxNew) | 0);
  var destPos = ((1 + idxNew) | 0);
  var length$1 = ((((src.a.length - idxNew) | 0) - 2) | 0);
  src.u(srcPos$1, dst, destPos, length$1);
  var dstHashes = this.o2(this.bt, dataIx);
  this.N = (this.N ^ bitpos);
  this.T = (this.T | bitpos);
  this.ae = dst;
  this.bt = dstHashes;
  this.aE = ((((this.aE - 1) | 0) + node.ax()) | 0);
  this.bd = ((((this.bd - keyHash) | 0) + node.dB()) | 0);
  return this;
});
$p.py = (function(bitpos, keyHash, node) {
  var dataIx = this.g0(bitpos);
  var idxOld = (dataIx << 1);
  var idxNew = ((((this.ae.a.length - 2) | 0) - this.jk(bitpos)) | 0);
  var src = this.ae;
  var dst = new $ac_O(((src.a.length - 1) | 0));
  src.u(0, dst, 0, idxOld);
  var srcPos = ((2 + idxOld) | 0);
  var length = ((idxNew - idxOld) | 0);
  src.u(srcPos, dst, idxOld, length);
  dst.a[idxNew] = node;
  var srcPos$1 = ((2 + idxNew) | 0);
  var destPos = ((1 + idxNew) | 0);
  var length$1 = ((((src.a.length - idxNew) | 0) - 2) | 0);
  src.u(srcPos$1, dst, destPos, length$1);
  var dstHashes = this.o2(this.bt, dataIx);
  return new $c_sci_BitmapIndexedMapNode((this.N ^ bitpos), (this.T | bitpos), dst, dstHashes, ((((this.aE - 1) | 0) + node.ax()) | 0), ((((this.bd - keyHash) | 0) + node.dB()) | 0));
});
$p.e1 = (function(f) {
  var iN = $m_jl_Integer$().dA(this.N);
  var i$1 = 0;
  while ((i$1 < iN)) {
    f.eM(this.cW(i$1), this.ct(i$1));
    i$1 = ((1 + i$1) | 0);
  }
  var jN = $m_jl_Integer$().dA(this.T);
  var j = 0;
  while ((j < jN)) {
    this.cs(j).e1(f);
    j = ((1 + j) | 0);
  }
});
$p.k = (function(that) {
  if ((that instanceof $c_sci_BitmapIndexedMapNode)) {
    if ((this === that)) {
      return true;
    } else if ((((((this.bd === that.bd) && (this.T === that.T)) && (this.N === that.N)) && (this.aE === that.aE)) && $m_ju_Arrays$().iU(this.bt, that.bt))) {
      var a1 = this.ae;
      var a2 = that.ae;
      var length = this.ae.a.length;
      if ((a1 === a2)) {
        return true;
      } else {
        var isEqual = true;
        var i = 0;
        while ((isEqual && (i < length))) {
          isEqual = $m_sr_BoxesRunTime$().j(a1.a[i], a2.a[i]);
          i = ((1 + i) | 0);
        }
        return isEqual;
      }
    } else {
      return false;
    }
  } else {
    return false;
  }
});
$p.r = (function() {
  throw new $c_jl_UnsupportedOperationException("Trie nodes do not support hashing.");
});
$p.t = (function() {
  var i = $systemIdentityHashCode(this);
  return (($objectClassName(this) + "@") + (i >>> 0.0).toString(16));
});
$p.nh = (function() {
  var this$1 = this.ae;
  var contentClone = this$1.e();
  var contentLength = contentClone.a.length;
  var i$1 = ($m_jl_Integer$().dA(this.N) << 1);
  while ((i$1 < contentLength)) {
    contentClone.a[i$1] = contentClone.a[i$1].ni();
    i$1 = ((1 + i$1) | 0);
  }
  return new $c_sci_BitmapIndexedMapNode(this.N, this.T, contentClone, this.bt.e(), this.aE, this.bd);
});
$p.j5 = (function(index) {
  return this.cs(index);
});
$p.on = (function(key, value, originalHash, hash, shift, replaceValue) {
  return this.om(key, value, originalHash, hash, shift, replaceValue);
});
$p.ni = (function() {
  return this.nh();
});
function $isArrayOf_sci_BitmapIndexedMapNode(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.c1)));
}
var $d_sci_BitmapIndexedMapNode = new $TypeData().i($c_sci_BitmapIndexedMapNode, "scala.collection.immutable.BitmapIndexedMapNode", ({
  c1: 1,
  ca: 1,
  aR: 1
}));
/** @constructor */
function $c_sci_HashCollisionMapNode(originalHash, hash, content) {
  this.ii = 0;
  this.dd = 0;
  this.a1 = null;
  this.ii = originalHash;
  this.dd = hash;
  this.a1 = content;
  $m_s_Predef$().r2((this.a1.q() >= 2));
}
$p = $c_sci_HashCollisionMapNode.prototype = new $h_sci_MapNode();
$p.constructor = $c_sci_HashCollisionMapNode;
/** @constructor */
function $h_sci_HashCollisionMapNode() {
}
$h_sci_HashCollisionMapNode.prototype = $p;
$p.eT = (function(key) {
  var iter = this.a1.i();
  var i = 0;
  while (iter.m()) {
    if ($m_sr_BoxesRunTime$().j(iter.g().aZ, key)) {
      return i;
    }
    i = ((1 + i) | 0);
  }
  return (-1);
});
$p.ax = (function() {
  return this.a1.q();
});
$p.iH = (function(key, originalHash, hash, shift) {
  var this$1 = this.h7(key, originalHash, hash, shift);
  return (this$1.c() ? $m_sc_Iterator$().O.g() : this$1.s());
});
$p.h7 = (function(key, originalHash, hash, shift) {
  if ((this.dd === hash)) {
    var index = this.eT(key);
    return ((index >= 0) ? new $c_s_Some(this.a1.v(index).aQ) : $m_s_None$());
  } else {
    return $m_s_None$();
  }
});
$p.j6 = (function(key, originalHash, hash, shift, f) {
  if ((this.dd === hash)) {
    var x36 = this.eT(key);
    if ((x36 === (-1))) {
      return f.F();
    }
    return this.a1.v(x36).aQ;
  } else {
    return f.F();
  }
});
$p.iP = (function(key, originalHash, hash, shift) {
  return ((this.dd === hash) && (this.eT(key) >= 0));
});
$p.on = (function(key, value, originalHash, hash, shift, replaceValue) {
  var index = this.eT(key);
  return ((index >= 0) ? (replaceValue ? (Object.is(this.a1.v(index).aQ, value) ? this : new $c_sci_HashCollisionMapNode(originalHash, hash, this.a1.dG(index, new $c_T2(key, value)))) : this) : new $c_sci_HashCollisionMapNode(originalHash, hash, this.a1.dz(new $c_T2(key, value))));
});
$p.j9 = (function() {
  return false;
});
$p.jj = (function() {
  return 0;
});
$p.cs = (function(index) {
  throw $ct_jl_IndexOutOfBoundsException__T__(new $c_jl_IndexOutOfBoundsException(), "No sub-nodes present in hash-collision leaf node.");
});
$p.h9 = (function() {
  return true;
});
$p.jo = (function() {
  return this.a1.q();
});
$p.cW = (function(index) {
  return this.a1.v(index).aZ;
});
$p.ct = (function(index) {
  return this.a1.v(index).aQ;
});
$p.nD = (function(index) {
  return this.a1.v(index);
});
$p.g3 = (function(index) {
  return this.ii;
});
$p.e1 = (function(f) {
  this.a1.bm(new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((x$1$2) => {
    var k = x$1$2.aZ;
    var v = x$1$2.aQ;
    return f.eM(k, v);
  })));
});
$p.k = (function(that) {
  if ((that instanceof $c_sci_HashCollisionMapNode)) {
    if ((this === that)) {
      return true;
    } else if (((this.dd === that.dd) && (this.a1.q() === that.a1.q()))) {
      var iter = this.a1.i();
      while (iter.m()) {
        var x47 = iter.g();
        var \u03b412$ = x47;
        var key$2 = \u03b412$.aZ;
        var value$2 = \u03b412$.aQ;
        var index = that.eT(key$2);
        if (((index < 0) || (!$m_sr_BoxesRunTime$().j(value$2, that.a1.v(index).aQ)))) {
          return false;
        }
      }
      return true;
    } else {
      return false;
    }
  } else {
    return false;
  }
});
$p.r = (function() {
  throw new $c_jl_UnsupportedOperationException("Trie nodes do not support hashing.");
});
$p.t = (function() {
  var i = $systemIdentityHashCode(this);
  return (($objectClassName(this) + "@") + (i >>> 0.0).toString(16));
});
$p.dB = (function() {
  return Math.imul(this.a1.q(), this.dd);
});
$p.j5 = (function(index) {
  return this.cs(index);
});
$p.ni = (function() {
  return new $c_sci_HashCollisionMapNode(this.ii, this.dd, this.a1);
});
function $isArrayOf_sci_HashCollisionMapNode(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.c3)));
}
var $d_sci_HashCollisionMapNode = new $TypeData().i($c_sci_HashCollisionMapNode, "scala.collection.immutable.HashCollisionMapNode", ({
  c3: 1,
  ca: 1,
  aR: 1
}));
/** @constructor */
function $c_sci_HashMap$() {
  this.ij = null;
  $n_sci_HashMap$ = this;
  this.ij = new $c_sci_HashMap($m_sci_MapNode$().mi);
}
$p = $c_sci_HashMap$.prototype = new $h_O();
$p.constructor = $c_sci_HashMap$;
/** @constructor */
function $h_sci_HashMap$() {
}
$h_sci_HashMap$.prototype = $p;
$p.q2 = (function(source) {
  return ((source instanceof $c_sci_HashMap) ? source : new $c_sci_HashMapBuilder().iG(source).jt());
});
$p.ag = (function(it) {
  return this.q2(it);
});
var $d_sci_HashMap$ = new $TypeData().i($c_sci_HashMap$, "scala.collection.immutable.HashMap$", ({
  fN: 1,
  a: 1,
  aL: 1
}));
var $n_sci_HashMap$;
function $m_sci_HashMap$() {
  if ((!$n_sci_HashMap$)) {
    $n_sci_HashMap$ = new $c_sci_HashMap$();
  }
  return $n_sci_HashMap$;
}
/** @constructor */
function $c_sci_Map$() {
}
$p = $c_sci_Map$.prototype = new $h_O();
$p.constructor = $c_sci_Map$;
/** @constructor */
function $h_sci_Map$() {
}
$h_sci_Map$.prototype = $p;
$p.nx = (function(it) {
  if ($is_sci_Iterable(it)) {
    if (it.c()) {
      return $m_sci_Map$EmptyMap$();
    }
  }
  if ((it instanceof $c_sci_HashMap)) {
    return it;
  }
  if ((it instanceof $c_sci_Map$Map1)) {
    return it;
  }
  if ((it instanceof $c_sci_Map$Map2)) {
    return it;
  }
  if ((it instanceof $c_sci_Map$Map3)) {
    return it;
  }
  if ((it instanceof $c_sci_Map$Map4)) {
    return it;
  }
  if (false) {
    return it;
  }
  if (false) {
    return it;
  }
  if (false) {
    return it;
  }
  if (false) {
    return it;
  }
  if (false) {
    return it;
  }
  if (false) {
    return it;
  }
  if (false) {
    return it;
  }
  return new $c_sci_MapBuilderImpl().mY(it).o6();
});
$p.ag = (function(it) {
  return this.nx(it);
});
var $d_sci_Map$ = new $TypeData().i($c_sci_Map$, "scala.collection.immutable.Map$", ({
  g2: 1,
  a: 1,
  aL: 1
}));
var $n_sci_Map$;
function $m_sci_Map$() {
  if ((!$n_sci_Map$)) {
    $n_sci_Map$ = new $c_sci_Map$();
  }
  return $n_sci_Map$;
}
function $f_scm_Builder__sizeHint__sc_IterableOnce__I__V($thiz, coll, delta) {
  var x1 = coll.x();
  if ((x1 === (-1))) {
    return (void 0);
  }
  var that = ((x1 + delta) | 0);
  $thiz.aX(((that < 0) ? 0 : that));
}
/** @constructor */
function $c_scm_HashSet$() {
}
$p = $c_scm_HashSet$.prototype = new $h_O();
$p.constructor = $c_scm_HashSet$;
/** @constructor */
function $h_scm_HashSet$() {
}
$h_scm_HashSet$.prototype = $p;
$p.q4 = (function(it) {
  var k = it.x();
  return $ct_scm_HashSet__I__D__(new $c_scm_HashSet(), ((k > 0) ? $doubleToInt((((1 + k) | 0) / 0.75)) : 16), 0.75).n1(it);
});
$p.aW = (function() {
  return new $c_scm_HashSet$$anon$4(16, 0.75);
});
$p.ag = (function(source) {
  return this.q4(source);
});
var $d_scm_HashSet$ = new $TypeData().i($c_scm_HashSet$, "scala.collection.mutable.HashSet$", ({
  gM: 1,
  a: 1,
  K: 1
}));
var $n_scm_HashSet$;
function $m_scm_HashSet$() {
  if ((!$n_scm_HashSet$)) {
    $n_scm_HashSet$ = new $c_scm_HashSet$();
  }
  return $n_scm_HashSet$;
}
/** @constructor */
function $c_s_concurrent_BatchingExecutor$SyncBatch(outer, runnable) {
  this.fH = null;
  this.fI = null;
  this.dv = 0;
  this.oC = null;
  if ((outer === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
  this.oC = outer;
  $ct_s_concurrent_BatchingExecutor$AbstractBatch__jl_Runnable__Ajl_Runnable__I__(this, runnable, $m_s_concurrent_BatchingExecutorStatics$().my, 1);
}
$p = $c_s_concurrent_BatchingExecutor$SyncBatch.prototype = new $h_s_concurrent_BatchingExecutor$AbstractBatch();
$p.constructor = $c_s_concurrent_BatchingExecutor$SyncBatch;
/** @constructor */
function $h_s_concurrent_BatchingExecutor$SyncBatch() {
}
$h_s_concurrent_BatchingExecutor$SyncBatch.prototype = $p;
$p.e8 = (function() {
  while (true) {
    try {
      this.r7(1024);
    } catch (e) {
      var e$2 = ((e instanceof $c_jl_Throwable) ? e : new $c_sjs_js_JavaScriptException(e));
      if (false) {
        $m_s_concurrent_ExecutionContext$().eG.b(e$2);
      } else {
        matchResult2: {
          if ($m_s_util_control_NonFatal$().gW(e$2)) {
            $m_s_concurrent_ExecutionContext$().eG.b(e$2);
            break matchResult2;
          }
          throw ((e$2 instanceof $c_sjs_js_JavaScriptException) ? e$2.K : e$2);
        }
      }
    }
    if ((this.dv > 0)) {
    } else {
      return (void 0);
    }
  }
});
function $isArrayOf_s_concurrent_BatchingExecutor$SyncBatch(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.cr)));
}
var $d_s_concurrent_BatchingExecutor$SyncBatch = new $TypeData().i($c_s_concurrent_BatchingExecutor$SyncBatch, "scala.concurrent.BatchingExecutor$SyncBatch", ({
  cr: 1,
  h3: 1,
  aE: 1
}));
/** @constructor */
function $c_s_concurrent_impl_Promise$Link(to) {
  this.L = null;
  $ct_ju_concurrent_atomic_AtomicReference__O__(this, to);
}
$p = $c_s_concurrent_impl_Promise$Link.prototype = new $h_ju_concurrent_atomic_AtomicReference();
$p.constructor = $c_s_concurrent_impl_Promise$Link;
/** @constructor */
function $h_s_concurrent_impl_Promise$Link() {
}
$h_s_concurrent_impl_Promise$Link.prototype = $p;
$p.eV = (function(owner) {
  var c = this.L;
  var target$tailLocal1 = c;
  var current$tailLocal1 = c;
  while (true) {
    var value = target$tailLocal1.L;
    if ($is_s_concurrent_impl_Promise$Callbacks(value)) {
      if (this.fY(current$tailLocal1, target$tailLocal1)) {
        return target$tailLocal1;
      } else {
        current$tailLocal1 = this.L;
      }
    } else if ((value instanceof $c_s_concurrent_impl_Promise$Link)) {
      target$tailLocal1 = value.L;
    } else {
      owner.rD(value);
      return owner;
    }
  }
});
function $isArrayOf_s_concurrent_impl_Promise$Link(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.cu)));
}
var $d_s_concurrent_impl_Promise$Link = new $TypeData().i($c_s_concurrent_impl_Promise$Link, "scala.concurrent.impl.Promise$Link", ({
  cu: 1,
  aG: 1,
  a: 1
}));
function $isArrayOf_s_math_ScalaNumber(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.hg)));
}
/** @constructor */
function $c_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c(f) {
  this.mG = null;
  this.mG = f;
}
$p = $c_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c.prototype = new $h_sr_AbstractFunction0();
$p.constructor = $c_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c;
/** @constructor */
function $h_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c() {
}
$h_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c.prototype = $p;
$p.F = (function() {
  return (0, this.mG)();
});
var $d_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c = new $TypeData().i($c_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c, "scala.runtime.AbstractFunction0.$$Lambda$07eded5776954a9c145e92c329afd52873ad179c", ({
  hF: 1,
  cx: 1,
  aH: 1
}));
/** @constructor */
function $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(f) {
  this.mH = null;
  this.mH = f;
}
$p = $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919.prototype = new $h_sr_AbstractFunction1();
$p.constructor = $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919;
/** @constructor */
function $h_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919() {
}
$h_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919.prototype = $p;
$p.b = (function(x0) {
  return (0, this.mH)(x0);
});
var $d_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919 = new $TypeData().i($c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919, "scala.runtime.AbstractFunction1.$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919", ({
  hG: 1,
  cy: 1,
  e: 1
}));
/** @constructor */
function $c_sr_AbstractFunction2_$$Lambda$b4228bd32034ae3b2f0c5fc896319aa4b79b55f8(f) {
  this.mI = null;
  this.mI = f;
}
$p = $c_sr_AbstractFunction2_$$Lambda$b4228bd32034ae3b2f0c5fc896319aa4b79b55f8.prototype = new $h_sr_AbstractFunction2();
$p.constructor = $c_sr_AbstractFunction2_$$Lambda$b4228bd32034ae3b2f0c5fc896319aa4b79b55f8;
/** @constructor */
function $h_sr_AbstractFunction2_$$Lambda$b4228bd32034ae3b2f0c5fc896319aa4b79b55f8() {
}
$h_sr_AbstractFunction2_$$Lambda$b4228bd32034ae3b2f0c5fc896319aa4b79b55f8.prototype = $p;
$p.eM = (function(x0, x1) {
  return (0, this.mI)(x0, x1);
});
var $d_sr_AbstractFunction2_$$Lambda$b4228bd32034ae3b2f0c5fc896319aa4b79b55f8 = new $TypeData().i($c_sr_AbstractFunction2_$$Lambda$b4228bd32034ae3b2f0c5fc896319aa4b79b55f8, "scala.runtime.AbstractFunction2.$$Lambda$b4228bd32034ae3b2f0c5fc896319aa4b79b55f8", ({
  hH: 1,
  cz: 1,
  aI: 1
}));
/** @constructor */
function $c_sr_AbstractPartialFunction() {
}
$p = $c_sr_AbstractPartialFunction.prototype = new $h_O();
$p.constructor = $c_sr_AbstractPartialFunction;
/** @constructor */
function $h_sr_AbstractPartialFunction() {
}
$h_sr_AbstractPartialFunction.prototype = $p;
$p.t = (function() {
  return "<function1>";
});
$p.b = (function(x) {
  return this.bX(x, $m_s_PartialFunction$().gC);
});
var $d_sr_Nothing$ = new $TypeData().i(0, "scala.runtime.Nothing$", ({
  hO: 1,
  s: 1,
  a: 1
}));
/** @constructor */
function $c_sjs_js_Any$() {
}
$p = $c_sjs_js_Any$.prototype = new $h_O();
$p.constructor = $c_sjs_js_Any$;
/** @constructor */
function $h_sjs_js_Any$() {
}
$h_sjs_js_Any$.prototype = $p;
$p.q5 = (function(f) {
  return (() => f.F());
});
$p.nA = (function(f) {
  return ((arg1$2) => f.b(arg1$2));
});
var $d_sjs_js_Any$ = new $TypeData().i($c_sjs_js_Any$, "scala.scalajs.js.Any$", ({
  i0: 1,
  i1: 1,
  i2: 1
}));
var $n_sjs_js_Any$;
function $m_sjs_js_Any$() {
  if ((!$n_sjs_js_Any$)) {
    $n_sjs_js_Any$ = new $c_sjs_js_Any$();
  }
  return $n_sjs_js_Any$;
}
/** @constructor */
function $c_sjsr_AnonFunction0() {
}
$p = $c_sjsr_AnonFunction0.prototype = new $h_sr_AbstractFunction0();
$p.constructor = $c_sjsr_AnonFunction0;
/** @constructor */
function $h_sjsr_AnonFunction0() {
}
$h_sjsr_AnonFunction0.prototype = $p;
/** @constructor */
function $c_sjsr_AnonFunction1() {
}
$p = $c_sjsr_AnonFunction1.prototype = new $h_sr_AbstractFunction1();
$p.constructor = $c_sjsr_AnonFunction1;
/** @constructor */
function $h_sjsr_AnonFunction1() {
}
$h_sjsr_AnonFunction1.prototype = $p;
/** @constructor */
function $c_sjsr_AnonFunction2() {
}
$p = $c_sjsr_AnonFunction2.prototype = new $h_sr_AbstractFunction2();
$p.constructor = $c_sjsr_AnonFunction2;
/** @constructor */
function $h_sjsr_AnonFunction2() {
}
$h_sjsr_AnonFunction2.prototype = $p;
/** @constructor */
function $c_sjsr_AnonFunction3() {
}
$p = $c_sjsr_AnonFunction3.prototype = new $h_sr_AbstractFunction3();
$p.constructor = $c_sjsr_AnonFunction3;
/** @constructor */
function $h_sjsr_AnonFunction3() {
}
$h_sjsr_AnonFunction3.prototype = $p;
/** @constructor */
function $c_sjsr_AnonFunction4() {
}
$p = $c_sjsr_AnonFunction4.prototype = new $h_sr_AbstractFunction4();
$p.constructor = $c_sjsr_AnonFunction4;
/** @constructor */
function $h_sjsr_AnonFunction4() {
}
$h_sjsr_AnonFunction4.prototype = $p;
function $isArrayOf_s_util_control_ControlThrowable(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.il)));
}
/** @constructor */
function $c_Lcom_raquo_airstream_core_Observer$$anon$8(onNextParam$2, handleObserverErrors$3, onErrorParam$2, outer) {
  this.jA = null;
  this.jy = false;
  this.hq = null;
  this.jz = null;
  this.jA = onNextParam$2;
  this.jy = handleObserverErrors$3;
  this.hq = onErrorParam$2;
  if ((outer === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
  this.jz = (void 0);
}
$p = $c_Lcom_raquo_airstream_core_Observer$$anon$8.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_airstream_core_Observer$$anon$8;
/** @constructor */
function $h_Lcom_raquo_airstream_core_Observer$$anon$8() {
}
$h_Lcom_raquo_airstream_core_Observer$$anon$8.prototype = $p;
$p.e3 = (function() {
  return this.jz;
});
$p.e0 = (function() {
  return $f_Lcom_raquo_airstream_core_Named__defaultDisplayName__T(this);
});
$p.t = (function() {
  return $f_Lcom_raquo_airstream_core_Named__displayName__T(this);
});
$p.jm = (function(nextValue) {
  try {
    this.jA.b(nextValue);
  } catch (e) {
    var e$2 = ((e instanceof $c_jl_Throwable) ? e : new $c_sjs_js_JavaScriptException(e));
    if (this.jy) {
      this.g9(new $c_Lcom_raquo_airstream_core_AirstreamError$ObserverError(e$2));
    } else {
      $m_Lcom_raquo_airstream_core_AirstreamError$().c2(new $c_Lcom_raquo_airstream_core_AirstreamError$ObserverError(e$2));
    }
  }
});
$p.g9 = (function(error) {
  try {
    if (this.hq.ca(error)) {
      this.hq.b(error);
    } else {
      $m_Lcom_raquo_airstream_core_AirstreamError$().c2(error);
    }
  } catch (e) {
    var e$2 = ((e instanceof $c_jl_Throwable) ? e : new $c_sjs_js_JavaScriptException(e));
    $m_Lcom_raquo_airstream_core_AirstreamError$().c2(new $c_Lcom_raquo_airstream_core_AirstreamError$ObserverErrorHandlingError(e$2, error));
  }
});
$p.e5 = (function(nextValue) {
  nextValue.c8(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((error) => {
    this.g9(error);
  })), new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((nextValue$2) => {
    this.jm(nextValue$2);
  })));
});
var $d_Lcom_raquo_airstream_core_Observer$$anon$8 = new $TypeData().i($c_Lcom_raquo_airstream_core_Observer$$anon$8, "com.raquo.airstream.core.Observer$$anon$8", ({
  cK: 1,
  aq: 1,
  a5: 1,
  aA: 1
}));
/** @constructor */
function $c_Lcom_raquo_airstream_core_Observer$$anon$9(onTryParam$2, handleObserverErrors$4, outer) {
  this.hr = null;
  this.jB = false;
  this.jC = null;
  this.hr = onTryParam$2;
  this.jB = handleObserverErrors$4;
  if ((outer === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
  this.jC = (void 0);
}
$p = $c_Lcom_raquo_airstream_core_Observer$$anon$9.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_airstream_core_Observer$$anon$9;
/** @constructor */
function $h_Lcom_raquo_airstream_core_Observer$$anon$9() {
}
$h_Lcom_raquo_airstream_core_Observer$$anon$9.prototype = $p;
$p.e3 = (function() {
  return this.jC;
});
$p.e0 = (function() {
  return $f_Lcom_raquo_airstream_core_Named__defaultDisplayName__T(this);
});
$p.t = (function() {
  return $f_Lcom_raquo_airstream_core_Named__displayName__T(this);
});
$p.jm = (function(nextValue) {
  this.e5(new $c_s_util_Success(nextValue));
});
$p.g9 = (function(error) {
  this.e5(new $c_s_util_Failure(error));
});
$p.e5 = (function(nextValue) {
  try {
    if (this.hr.ca(nextValue)) {
      this.hr.b(nextValue);
    } else {
      nextValue.c8(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((err) => {
        $m_Lcom_raquo_airstream_core_AirstreamError$().c2(err);
      })), new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((_$3) => (void 0))));
    }
  } catch (e) {
    var e$2 = ((e instanceof $c_jl_Throwable) ? e : new $c_sjs_js_JavaScriptException(e));
    if ((this.jB && nextValue.nI())) {
      this.g9(new $c_Lcom_raquo_airstream_core_AirstreamError$ObserverError(e$2));
    } else {
      nextValue.c8(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((originalError) => {
        $m_Lcom_raquo_airstream_core_AirstreamError$().c2(new $c_Lcom_raquo_airstream_core_AirstreamError$ObserverErrorHandlingError(e$2, originalError));
      })), new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((_$4) => {
        $m_Lcom_raquo_airstream_core_AirstreamError$().c2(new $c_Lcom_raquo_airstream_core_AirstreamError$ObserverError(e$2));
      })));
    }
  }
});
var $d_Lcom_raquo_airstream_core_Observer$$anon$9 = new $TypeData().i($c_Lcom_raquo_airstream_core_Observer$$anon$9, "com.raquo.airstream.core.Observer$$anon$9", ({
  cL: 1,
  aq: 1,
  a5: 1,
  aA: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_api_Laminar$svg$(outer) {
  this.ks = null;
  this.kt = false;
  this.or = null;
  if ((outer === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
  $f_Lcom_raquo_laminar_defs_complex_ComplexSvgKeys__$init$__V(this);
}
$p = $c_Lcom_raquo_laminar_api_Laminar$svg$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_api_Laminar$svg$;
/** @constructor */
function $h_Lcom_raquo_laminar_api_Laminar$svg$() {
}
$h_Lcom_raquo_laminar_api_Laminar$svg$.prototype = $p;
$p.rn = (function() {
  if ((!this.kt)) {
    this.ks = new $c_Lcom_raquo_laminar_tags_SvgTag("svg", false);
    this.kt = true;
  }
  return this.ks;
});
var $d_Lcom_raquo_laminar_api_Laminar$svg$ = new $TypeData().i($c_Lcom_raquo_laminar_api_Laminar$svg$, "com.raquo.laminar.api.Laminar$svg$", ({
  dl: 1,
  dC: 1,
  dv: 1,
  dx: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_api_package$() {
  this.o = null;
  $n_Lcom_raquo_laminar_api_package$ = this;
  this.o = new $c_Lcom_raquo_laminar_api_package$$anon$1();
}
$p = $c_Lcom_raquo_laminar_api_package$.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_api_package$;
/** @constructor */
function $h_Lcom_raquo_laminar_api_package$() {
}
$h_Lcom_raquo_laminar_api_package$.prototype = $p;
var $d_Lcom_raquo_laminar_api_package$ = new $TypeData().i($c_Lcom_raquo_laminar_api_package$, "com.raquo.laminar.api.package$", ({
  dq: 1,
  bd: 1,
  bg: 1,
  bc: 1
}));
var $n_Lcom_raquo_laminar_api_package$;
function $m_Lcom_raquo_laminar_api_package$() {
  if ((!$n_Lcom_raquo_laminar_api_package$)) {
    $n_Lcom_raquo_laminar_api_package$ = new $c_Lcom_raquo_laminar_api_package$();
  }
  return $n_Lcom_raquo_laminar_api_package$;
}
/** @constructor */
function $c_Lcom_raquo_laminar_inserters_DynamicInserter(initialContext, preferStrictMode, insertFn, hooks) {
  this.ls = null;
  this.lu = false;
  this.lt = null;
  this.hI = null;
  this.ls = initialContext;
  this.lu = preferStrictMode;
  this.lt = insertFn;
  this.hI = hooks;
}
$p = $c_Lcom_raquo_laminar_inserters_DynamicInserter.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_inserters_DynamicInserter;
/** @constructor */
function $h_Lcom_raquo_laminar_inserters_DynamicInserter() {
}
$h_Lcom_raquo_laminar_inserters_DynamicInserter.prototype = $p;
$p.iL = (function(element) {
  var this$1 = this.ls;
  var insertContext = (this$1.c() ? $m_Lcom_raquo_laminar_inserters_InsertContext$().r3(element, this.lu, this.hI) : this$1.s());
  var subscribe = new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((mountContext) => this.lt.iI(insertContext, mountContext.hQ, this.hI)));
  return $m_Lcom_raquo_airstream_ownership_DynamicSubscription$().gk(element.c4, new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((owner) => subscribe.b(new $c_Lcom_raquo_laminar_lifecycle_MountContext(element, owner)))), false);
});
$p.co = (function(element) {
  this.iL(element);
});
var $d_Lcom_raquo_laminar_inserters_DynamicInserter = new $TypeData().i($c_Lcom_raquo_laminar_inserters_DynamicInserter, "com.raquo.laminar.inserters.DynamicInserter", ({
  dH: 1,
  X: 1,
  dL: 1,
  dI: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_nodes_CommentNode(initialText) {
  this.hV = null;
  this.hW = null;
  this.hV = $m_s_None$();
  this.hW = $m_Lcom_raquo_laminar_DomApi$().pB(initialText);
}
$p = $c_Lcom_raquo_laminar_nodes_CommentNode.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_nodes_CommentNode;
/** @constructor */
function $h_Lcom_raquo_laminar_nodes_CommentNode() {
}
$h_Lcom_raquo_laminar_nodes_CommentNode.prototype = $p;
$p.iM = (function() {
  return this.hV;
});
$p.e9 = (function(maybeNextParent) {
  this.hV = maybeNextParent;
});
$p.ec = (function(maybeNextParent) {
});
$p.co = (function(parentNode) {
  $m_Lcom_raquo_laminar_nodes_ParentNode$().eL(parentNode, this, (void 0));
});
$p.I = (function() {
  return this.hW;
});
var $d_Lcom_raquo_laminar_nodes_CommentNode = new $TypeData().i($c_Lcom_raquo_laminar_nodes_CommentNode, "com.raquo.laminar.nodes.CommentNode", ({
  ed: 1,
  as: 1,
  X: 1,
  aC: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_nodes_TextNode(initialText) {
  this.i1 = null;
  this.gz = null;
  this.i1 = $m_s_None$();
  this.gz = $m_Lcom_raquo_laminar_DomApi$().pE(initialText);
}
$p = $c_Lcom_raquo_laminar_nodes_TextNode.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_nodes_TextNode;
/** @constructor */
function $h_Lcom_raquo_laminar_nodes_TextNode() {
}
$h_Lcom_raquo_laminar_nodes_TextNode.prototype = $p;
$p.iM = (function() {
  return this.i1;
});
$p.e9 = (function(maybeNextParent) {
  this.i1 = maybeNextParent;
});
$p.ec = (function(maybeNextParent) {
});
$p.co = (function(parentNode) {
  $m_Lcom_raquo_laminar_nodes_ParentNode$().eL(parentNode, this, (void 0));
});
$p.rw = (function() {
  return this.gz.data;
});
$p.I = (function() {
  return this.gz;
});
var $d_Lcom_raquo_laminar_nodes_TextNode = new $TypeData().i($c_Lcom_raquo_laminar_nodes_TextNode, "com.raquo.laminar.nodes.TextNode", ({
  ej: 1,
  as: 1,
  X: 1,
  aC: 1
}));
/** @constructor */
function $c_Ldpm_Main$Answer(columns, rows, millis_$_lo, millis_$_hi, sql, source) {
  this.el = null;
  this.dN = null;
  this.eH = 0;
  this.eI = 0;
  this.en = null;
  this.em = null;
  this.el = columns;
  this.dN = rows;
  this.eH = millis_$_lo;
  this.eI = millis_$_hi;
  this.en = sql;
  this.em = source;
}
$p = $c_Ldpm_Main$Answer.prototype = new $h_O();
$p.constructor = $c_Ldpm_Main$Answer;
/** @constructor */
function $h_Ldpm_Main$Answer() {
}
$h_Ldpm_Main$Answer.prototype = $p;
$p.bx = (function() {
  return new $c_s_Product$$anon$1(this);
});
$p.r = (function() {
  var acc = (-889275714);
  acc = $m_sr_Statics$().w(acc, 1966025694);
  acc = $m_sr_Statics$().w(acc, $m_sr_Statics$().C(this.el));
  acc = $m_sr_Statics$().w(acc, $m_sr_Statics$().C(this.dN));
  acc = $m_sr_Statics$().w(acc, $m_sr_Statics$().nO(this.eH, this.eI));
  acc = $m_sr_Statics$().w(acc, $m_sr_Statics$().C(this.en));
  acc = $m_sr_Statics$().w(acc, $m_sr_Statics$().C(this.em));
  return $m_sr_Statics$().ar(acc, 5);
});
$p.k = (function(x$0) {
  if ((this === x$0)) {
    return true;
  } else if ((x$0 instanceof $c_Ldpm_Main$Answer)) {
    var x_$_lo = this.eH;
    var x_$_hi = this.eI;
    var $x_3 = x$0;
    var x$1_$_lo = $x_3.eH;
    var x$1_$_hi = $x_3.eI;
    if ((((x_$_lo ^ x$1_$_lo) | (x_$_hi ^ x$1_$_hi)) === 0)) {
      var x$2 = this.el;
      var x$2$1 = x$0.el;
      var $x_2 = ((x$2 === null) ? (x$2$1 === null) : x$2.k(x$2$1));
    } else {
      var $x_2 = false;
    }
    if ($x_2) {
      var x$3 = this.dN;
      var x$4 = x$0.dN;
      var $x_1 = ((x$3 === null) ? (x$4 === null) : x$3.k(x$4));
    } else {
      var $x_1 = false;
    }
    if (($x_1 && (this.en === x$0.en))) {
      return (this.em === x$0.em);
    } else {
      return false;
    }
  } else {
    return false;
  }
});
$p.t = (function() {
  return $m_sr_ScalaRunTime$().eK(this);
});
$p.aN = (function() {
  return 5;
});
$p.aP = (function() {
  return "Answer";
});
$p.aO = (function(n) {
  switch (n) {
    case 0: {
      return this.el;
      break;
    }
    case 1: {
      return this.dN;
      break;
    }
    case 2: {
      return $bL(this.eH, this.eI);
      break;
    }
    case 3: {
      return this.en;
      break;
    }
    case 4: {
      return this.em;
      break;
    }
    default: {
      throw $ct_jl_IndexOutOfBoundsException__I__(new $c_jl_IndexOutOfBoundsException(), n);
    }
  }
});
function $isArrayOf_Ldpm_Main$Answer(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.bm)));
}
var $d_Ldpm_Main$Answer = new $TypeData().i($c_Ldpm_Main$Answer, "dpm.Main$Answer", ({
  bm: 1,
  d: 1,
  E: 1,
  a: 1
}));
/** @constructor */
function $c_Ldpm_Question(id, ask, slots, sql, reads) {
  this.eo = null;
  this.fg = null;
  this.ep = null;
  this.fi = null;
  this.fh = null;
  this.eo = id;
  this.fg = ask;
  this.ep = slots;
  this.fi = sql;
  this.fh = reads;
}
$p = $c_Ldpm_Question.prototype = new $h_O();
$p.constructor = $c_Ldpm_Question;
/** @constructor */
function $h_Ldpm_Question() {
}
$h_Ldpm_Question.prototype = $p;
$p.bx = (function() {
  return new $c_s_Product$$anon$1(this);
});
$p.r = (function() {
  return $m_s_util_hashing_MurmurHash3$().e7(this, 1465040773, true);
});
$p.k = (function(x$0) {
  if ((this === x$0)) {
    return true;
  } else if ((x$0 instanceof $c_Ldpm_Question)) {
    if (((this.eo === x$0.eo) && (this.fg === x$0.fg))) {
      var x = this.ep;
      var x$2 = x$0.ep;
      var $x_2 = ((x === null) ? (x$2 === null) : x.k(x$2));
    } else {
      var $x_2 = false;
    }
    if ($x_2) {
      var x$3 = this.fi;
      var x$4 = x$0.fi;
      var $x_1 = ((x$3 === null) ? (x$4 === null) : x$3.k(x$4));
    } else {
      var $x_1 = false;
    }
    if ($x_1) {
      var x$5 = this.fh;
      var x$6 = x$0.fh;
      return ((x$5 === null) ? (x$6 === null) : x$5.k(x$6));
    } else {
      return false;
    }
  } else {
    return false;
  }
});
$p.t = (function() {
  return $m_sr_ScalaRunTime$().eK(this);
});
$p.aN = (function() {
  return 5;
});
$p.aP = (function() {
  return "Question";
});
$p.aO = (function(n) {
  switch (n) {
    case 0: {
      return this.eo;
      break;
    }
    case 1: {
      return this.fg;
      break;
    }
    case 2: {
      return this.ep;
      break;
    }
    case 3: {
      return this.fi;
      break;
    }
    case 4: {
      return this.fh;
      break;
    }
    default: {
      throw $ct_jl_IndexOutOfBoundsException__I__(new $c_jl_IndexOutOfBoundsException(), n);
    }
  }
});
$p.rg = (function(filled) {
  return this.fh.b(filled.b("framework"));
});
function $isArrayOf_Ldpm_Question(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.bn)));
}
var $d_Ldpm_Question = new $TypeData().i($c_Ldpm_Question, "dpm.Question", ({
  bn: 1,
  d: 1,
  E: 1,
  a: 1
}));
/** @constructor */
function $c_Ldpm_Slot(name, label, placeholder, example) {
  this.dO = null;
  this.fk = null;
  this.fl = null;
  this.eq = null;
  this.dO = name;
  this.fk = label;
  this.fl = placeholder;
  this.eq = example;
}
$p = $c_Ldpm_Slot.prototype = new $h_O();
$p.constructor = $c_Ldpm_Slot;
/** @constructor */
function $h_Ldpm_Slot() {
}
$h_Ldpm_Slot.prototype = $p;
$p.bx = (function() {
  return new $c_s_Product$$anon$1(this);
});
$p.r = (function() {
  return $m_s_util_hashing_MurmurHash3$().e7(this, 1691081175, true);
});
$p.k = (function(x$0) {
  return ((this === x$0) || ((x$0 instanceof $c_Ldpm_Slot) && ((((this.dO === x$0.dO) && (this.fk === x$0.fk)) && (this.fl === x$0.fl)) && (this.eq === x$0.eq))));
});
$p.t = (function() {
  return $m_sr_ScalaRunTime$().eK(this);
});
$p.aN = (function() {
  return 4;
});
$p.aP = (function() {
  return "Slot";
});
$p.aO = (function(n) {
  switch (n) {
    case 0: {
      return this.dO;
      break;
    }
    case 1: {
      return this.fk;
      break;
    }
    case 2: {
      return this.fl;
      break;
    }
    case 3: {
      return this.eq;
      break;
    }
    default: {
      throw $ct_jl_IndexOutOfBoundsException__I__(new $c_jl_IndexOutOfBoundsException(), n);
    }
  }
});
function $isArrayOf_Ldpm_Slot(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.bo)));
}
var $d_Ldpm_Slot = new $TypeData().i($c_Ldpm_Slot, "dpm.Slot", ({
  bo: 1,
  d: 1,
  E: 1,
  a: 1
}));
/** @constructor */
function $c_Ljava_io_OutputStream() {
}
$p = $c_Ljava_io_OutputStream.prototype = new $h_O();
$p.constructor = $c_Ljava_io_OutputStream;
/** @constructor */
function $h_Ljava_io_OutputStream() {
}
$h_Ljava_io_OutputStream.prototype = $p;
function $f_jl_Boolean__equals__O__Z($thiz, that) {
  return ($thiz === that);
}
function $f_jl_Boolean__hashCode__I($thiz) {
  return ($thiz ? 1231 : 1237);
}
function $f_jl_Boolean__toString__T($thiz) {
  return ("" + $thiz);
}
var $d_jl_Boolean = new $TypeData().i(0, "java.lang.Boolean", ({
  ex: 1,
  a: 1,
  a1: 1,
  Y: 1
}), ((x) => ((typeof x) === "boolean")));
function $f_jl_Character__hashCode__I($thiz) {
  return $thiz;
}
function $f_jl_Character__equals__O__Z($thiz, that) {
  return ((that instanceof $Char) && ($thiz === that.c));
}
function $f_jl_Character__toString__T($thiz) {
  return ("" + $cToS($thiz));
}
function $isArrayOf_jl_Character(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.bu)));
}
var $d_jl_Character = new $TypeData().i(0, "java.lang.Character", ({
  bu: 1,
  a: 1,
  a1: 1,
  Y: 1
}), ((x) => (x instanceof $Char)));
function $isArrayOf_jl_InterruptedException(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.eG)));
}
function $isArrayOf_jl_LinkageError(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.eJ)));
}
function $ct_jl_RuntimeException__T__($thiz, s) {
  $ct_jl_Throwable__T__jl_Throwable__Z__Z__($thiz, s, null, true, true);
  return $thiz;
}
class $c_jl_RuntimeException extends $c_jl_Exception {
}
var $d_jl_RuntimeException = new $TypeData().i($c_jl_RuntimeException, "java.lang.RuntimeException", ({
  D: 1,
  B: 1,
  s: 1,
  a: 1
}));
function $ct_jl_StringBuilder__($thiz) {
  $thiz.p = "";
  return $thiz;
}
function $ct_jl_StringBuilder__T__($thiz, str) {
  $ct_jl_StringBuilder__($thiz);
  $thiz.p = str;
  return $thiz;
}
function $ct_jl_StringBuilder__I__($thiz, initialCapacity) {
  $ct_jl_StringBuilder__($thiz);
  return $thiz;
}
/** @constructor */
function $c_jl_StringBuilder() {
  this.p = null;
}
$p = $c_jl_StringBuilder.prototype = new $h_O();
$p.constructor = $c_jl_StringBuilder;
/** @constructor */
function $h_jl_StringBuilder() {
}
$h_jl_StringBuilder.prototype = $p;
$p.n4 = (function(str) {
  var str$1 = $m_jl_String$().qE(str, 0, str.a.length);
  this.p = (("" + this.p) + str$1);
  return this;
});
$p.t = (function() {
  return this.p;
});
$p.q = (function() {
  return this.p.length;
});
$p.nc = (function(index) {
  return this.p.charCodeAt(index);
});
var $d_jl_StringBuilder = new $TypeData().i($c_jl_StringBuilder, "java.lang.StringBuilder", ({
  eS: 1,
  aD: 1,
  bs: 1,
  a: 1
}));
function $isArrayOf_jl_ThreadDeath(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.eV)));
}
class $c_jl_VirtualMachineError extends $c_jl_Error {
}
function $isArrayOf_jl_VirtualMachineError(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.bC)));
}
class $c_ju_concurrent_ExecutionException extends $c_jl_Exception {
  constructor(message, cause) {
    super();
    $ct_jl_Throwable__T__jl_Throwable__Z__Z__(this, message, cause, true, true);
  }
}
var $d_ju_concurrent_ExecutionException = new $TypeData().i($c_ju_concurrent_ExecutionException, "java.util.concurrent.ExecutionException", ({
  f2: 1,
  B: 1,
  s: 1,
  a: 1
}));
/** @constructor */
function $c_s_PartialFunction$$anon$1() {
}
$p = $c_s_PartialFunction$$anon$1.prototype = new $h_O();
$p.constructor = $c_s_PartialFunction$$anon$1;
/** @constructor */
function $h_s_PartialFunction$$anon$1() {
}
$h_s_PartialFunction$$anon$1.prototype = $p;
$p.t = (function() {
  return "<function1>";
});
$p.bX = (function(x, default$1) {
  return $f_s_PartialFunction__applyOrElse__O__F1__O(this, x, default$1);
});
$p.ca = (function(x) {
  return false;
});
$p.iJ = (function(x) {
  throw new $c_s_MatchError(x);
});
$p.b = (function(v1) {
  this.iJ(v1);
});
var $d_s_PartialFunction$$anon$1 = new $TypeData().i($c_s_PartialFunction$$anon$1, "scala.PartialFunction$$anon$1", ({
  fe: 1,
  e: 1,
  j: 1,
  a: 1
}));
/** @constructor */
function $c_sc_AbstractIterator() {
}
$p = $c_sc_AbstractIterator.prototype = new $h_O();
$p.constructor = $c_sc_AbstractIterator;
/** @constructor */
function $h_sc_AbstractIterator() {
}
$h_sc_AbstractIterator.prototype = $p;
$p.x = (function() {
  return (-1);
});
$p.bI = (function(dest, start, n) {
  return $f_sc_IterableOnceOps__copyToArray__O__I__I__I(this, dest, start, n);
});
$p.dy = (function(b, start, sep, end) {
  return $f_sc_IterableOnceOps__addString__scm_StringBuilder__T__T__T__scm_StringBuilder(this, b, start, sep, end);
});
$p.i = (function() {
  return this;
});
$p.iO = (function(xs) {
  return $f_sc_Iterator__concat__F0__sc_Iterator(this, xs);
});
$p.dC = (function(n) {
  return this.gg(n, (-1));
});
$p.gg = (function(from, until) {
  return $f_sc_Iterator__sliceIterator__I__I__sc_Iterator(this, from, until);
});
$p.t = (function() {
  return "<iterator>";
});
/** @constructor */
function $c_sc_Map$() {
  this.ig = null;
  this.m7 = null;
  this.m8 = null;
  $ct_sc_MapFactory$Delegate__sc_MapFactory__(this, $m_sci_Map$());
  $n_sc_Map$ = this;
  this.m7 = $ct_O__(new $c_O());
  this.m8 = new $c_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c((() => this.m7));
}
$p = $c_sc_Map$.prototype = new $h_sc_MapFactory$Delegate();
$p.constructor = $c_sc_Map$;
/** @constructor */
function $h_sc_Map$() {
}
$h_sc_Map$.prototype = $p;
var $d_sc_Map$ = new $TypeData().i($c_sc_Map$, "scala.collection.Map$", ({
  fz: 1,
  fA: 1,
  a: 1,
  aL: 1
}));
var $n_sc_Map$;
function $m_sc_Map$() {
  if ((!$n_sc_Map$)) {
    $n_sc_Map$ = new $c_sc_Map$();
  }
  return $n_sc_Map$;
}
function $ct_sc_SeqFactory$Delegate__sc_SeqFactory__($thiz, delegate) {
  $thiz.ew = delegate;
  return $thiz;
}
/** @constructor */
function $c_sc_SeqFactory$Delegate() {
  this.ew = null;
}
$p = $c_sc_SeqFactory$Delegate.prototype = new $h_O();
$p.constructor = $c_sc_SeqFactory$Delegate;
/** @constructor */
function $h_sc_SeqFactory$Delegate() {
}
$h_sc_SeqFactory$Delegate.prototype = $p;
$p.nb = (function(elems) {
  return this.ew.cT(elems);
});
$p.nv = (function(it) {
  return this.ew.ag(it);
});
$p.aW = (function() {
  return this.ew.aW();
});
$p.cT = (function(elems) {
  return this.nb(elems);
});
$p.ag = (function(source) {
  return this.nv(source);
});
function $f_sc_SeqOps__distinct__O($thiz) {
  return $thiz.cq(new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((x$2) => x$2)));
}
function $f_sc_SeqOps__distinctBy__F1__O($thiz, f) {
  return $thiz.g2(new $c_sc_View$DistinctBy($thiz, f));
}
function $f_sc_SeqOps__isDefinedAt__I__Z($thiz, idx) {
  return ((idx >= 0) && ($thiz.bc(idx) > 0));
}
function $f_sc_SeqOps__isEmpty__Z($thiz) {
  return ($thiz.bc(0) === 0);
}
function $f_sc_SeqOps__sameElements__sc_IterableOnce__Z($thiz, that) {
  var thisKnownSize = $thiz.x();
  if ((thisKnownSize !== (-1))) {
    var thatKnownSize = that.x();
    if ((thatKnownSize !== (-1))) {
      if ((thisKnownSize !== thatKnownSize)) {
        return false;
      }
      if ((thisKnownSize === 0)) {
        return true;
      }
    }
  }
  return $f_sc_Iterator__sameElements__sc_IterableOnce__Z($thiz.i(), that);
}
/** @constructor */
function $c_sci_Iterable$() {
  this.gE = null;
  $ct_sc_IterableFactory$Delegate__sc_IterableFactory__(this, $m_sci_List$());
}
$p = $c_sci_Iterable$.prototype = new $h_sc_IterableFactory$Delegate();
$p.constructor = $c_sci_Iterable$;
/** @constructor */
function $h_sci_Iterable$() {
}
$h_sci_Iterable$.prototype = $p;
$p.q3 = (function(it) {
  return ($is_sci_Iterable(it) ? it : $c_sc_IterableFactory$Delegate.prototype.ag.call(this, it));
});
$p.ag = (function(it) {
  return this.q3(it);
});
var $d_sci_Iterable$ = new $TypeData().i($c_sci_Iterable$, "scala.collection.immutable.Iterable$", ({
  fS: 1,
  fq: 1,
  a: 1,
  K: 1
}));
var $n_sci_Iterable$;
function $m_sci_Iterable$() {
  if ((!$n_sci_Iterable$)) {
    $n_sci_Iterable$ = new $c_sci_Iterable$();
  }
  return $n_sci_Iterable$;
}
/** @constructor */
function $c_sci_LazyList$() {
  this.a2 = null;
  $n_sci_LazyList$ = this;
  this.a2 = $ct_sci_LazyList__O__(new $c_sci_LazyList(), $m_sci_LazyList$EmptyMarker$());
}
$p = $c_sci_LazyList$.prototype = new $h_O();
$p.constructor = $c_sci_LazyList$;
/** @constructor */
function $h_sci_LazyList$() {
}
$h_sci_LazyList$.prototype = $p;
$p.cT = (function(elems) {
  return this.j2(elems);
});
$p.r8 = (function(ll, n) {
  return $ct_sci_LazyList__O__(new $c_sci_LazyList(), new $c_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c(((restRef, iRef) => (() => {
    var rest = restRef.R;
    var i = iRef.ab;
    while (((i > 0) && (!($p_sci_LazyList__evaluated__sci_LazyList(rest) === $m_sci_LazyList$().a2)))) {
      rest = rest.b3();
      restRef.R = rest;
      i = ((i - 1) | 0);
      iRef.ab = i;
    }
    return rest;
  }))(new $c_sr_ObjectRef(ll), new $c_sr_IntRef(n))));
});
$p.j2 = (function(coll) {
  return ((coll instanceof $c_sci_LazyList) ? coll : ((coll.x() === 0) ? this.a2 : $ct_sci_LazyList__O__(new $c_sci_LazyList(), new $c_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c((() => this.o8(coll.i()))))));
});
$p.o9 = (function(it, suffix) {
  return (it.m() ? $ct_sci_LazyList__O__sci_LazyList__(new $c_sci_LazyList(), it.g(), $ct_sci_LazyList__O__(new $c_sci_LazyList(), new $c_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c((() => this.o9(it, suffix))))) : suffix.F());
});
$p.o8 = (function(it) {
  return (it.m() ? $ct_sci_LazyList__O__sci_LazyList__(new $c_sci_LazyList(), it.g(), $ct_sci_LazyList__O__(new $c_sci_LazyList(), new $c_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c((() => this.o8(it))))) : this.a2);
});
$p.aW = (function() {
  return new $c_sci_LazyList$LazyBuilder();
});
$p.ag = (function(source) {
  return this.j2(source);
});
var $d_sci_LazyList$ = new $TypeData().i($c_sci_LazyList$, "scala.collection.immutable.LazyList$", ({
  fT: 1,
  a: 1,
  K: 1,
  a0: 1
}));
var $n_sci_LazyList$;
function $m_sci_LazyList$() {
  if ((!$n_sci_LazyList$)) {
    $n_sci_LazyList$ = new $c_sci_LazyList$();
  }
  return $n_sci_LazyList$;
}
/** @constructor */
function $c_scm_Builder$$anon$1(f$2, outer) {
  this.ms = null;
  this.fD = null;
  this.ms = f$2;
  if ((outer === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
  this.fD = outer;
}
$p = $c_scm_Builder$$anon$1.prototype = new $h_O();
$p.constructor = $c_scm_Builder$$anon$1;
/** @constructor */
function $h_scm_Builder$$anon$1() {
}
$h_scm_Builder$$anon$1.prototype = $p;
$p.p3 = (function(x) {
  this.fD.aV(x);
  return this;
});
$p.oT = (function(xs) {
  this.fD.aU(xs);
  return this;
});
$p.aX = (function(size) {
  this.fD.aX(size);
});
$p.b2 = (function() {
  return this.ms.b(this.fD.b2());
});
$p.aV = (function(elem) {
  return this.p3(elem);
});
$p.aU = (function(elems) {
  return this.oT(elems);
});
var $d_scm_Builder$$anon$1 = new $TypeData().i($c_scm_Builder$$anon$1, "scala.collection.mutable.Builder$$anon$1", ({
  gJ: 1,
  G: 1,
  I: 1,
  M: 1
}));
function $ct_scm_GrowableBuilder__scm_Growable__($thiz, elems) {
  $thiz.ds = elems;
  return $thiz;
}
/** @constructor */
function $c_scm_GrowableBuilder() {
  this.ds = null;
}
$p = $c_scm_GrowableBuilder.prototype = new $h_O();
$p.constructor = $c_scm_GrowableBuilder;
/** @constructor */
function $h_scm_GrowableBuilder() {
}
$h_scm_GrowableBuilder.prototype = $p;
$p.aX = (function(size) {
});
$p.p4 = (function(elem) {
  this.ds.aV(elem);
  return this;
});
$p.oU = (function(xs) {
  this.ds.aU(xs);
  return this;
});
$p.b2 = (function() {
  return this.ds;
});
$p.aV = (function(elem) {
  return this.p4(elem);
});
$p.aU = (function(elems) {
  return this.oU(elems);
});
var $d_scm_GrowableBuilder = new $TypeData().i($c_scm_GrowableBuilder, "scala.collection.mutable.GrowableBuilder", ({
  aU: 1,
  G: 1,
  I: 1,
  M: 1
}));
class $c_s_concurrent_Future$$anon$4 extends $c_jl_Throwable {
  constructor() {
    super();
    $ct_jl_Throwable__T__jl_Throwable__Z__Z__(this, null, null, true, true);
  }
  eP() {
    return $f_s_util_control_NoStackTrace__fillInStackTrace__jl_Throwable(this);
  }
}
var $d_s_concurrent_Future$$anon$4 = new $TypeData().i($c_s_concurrent_Future$$anon$4, "scala.concurrent.Future$$anon$4", ({
  hb: 1,
  s: 1,
  a: 1,
  ay: 1
}));
function $isArrayOf_sr_NonLocalReturnControl(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.hN)));
}
/** @constructor */
function $c_sjs_concurrent_QueueExecutionContext$PromisesExecutionContext() {
  this.mM = null;
  this.mM = Promise.resolve((void 0));
}
$p = $c_sjs_concurrent_QueueExecutionContext$PromisesExecutionContext.prototype = new $h_O();
$p.constructor = $c_sjs_concurrent_QueueExecutionContext$PromisesExecutionContext;
/** @constructor */
function $h_sjs_concurrent_QueueExecutionContext$PromisesExecutionContext() {
}
$h_sjs_concurrent_QueueExecutionContext$PromisesExecutionContext.prototype = $p;
$p.iW = (function(runnable) {
  this.mM.then(((arg1$2) => {
    try {
      runnable.e8();
    } catch (e) {
      ((e instanceof $c_jl_Throwable) ? e : new $c_sjs_js_JavaScriptException(e)).gc($m_jl_System$Streams$().ev);
    }
  }));
});
$p.js = (function(t) {
  t.gc($m_jl_System$Streams$().ev);
});
var $d_sjs_concurrent_QueueExecutionContext$PromisesExecutionContext = new $TypeData().i($c_sjs_concurrent_QueueExecutionContext$PromisesExecutionContext, "scala.scalajs.concurrent.QueueExecutionContext$PromisesExecutionContext", ({
  hY: 1,
  aX: 1,
  aW: 1,
  aF: 1
}));
/** @constructor */
function $c_sjs_concurrent_QueueExecutionContext$TimeoutsExecutionContext() {
}
$p = $c_sjs_concurrent_QueueExecutionContext$TimeoutsExecutionContext.prototype = new $h_O();
$p.constructor = $c_sjs_concurrent_QueueExecutionContext$TimeoutsExecutionContext;
/** @constructor */
function $h_sjs_concurrent_QueueExecutionContext$TimeoutsExecutionContext() {
}
$h_sjs_concurrent_QueueExecutionContext$TimeoutsExecutionContext.prototype = $p;
$p.iW = (function(runnable) {
  setTimeout($m_sjs_js_Any$().q5(new $c_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c((() => {
    try {
      runnable.e8();
    } catch (e) {
      ((e instanceof $c_jl_Throwable) ? e : new $c_sjs_js_JavaScriptException(e)).gc($m_jl_System$Streams$().ev);
    }
  }))), 0);
});
$p.js = (function(t) {
  t.gc($m_jl_System$Streams$().ev);
});
var $d_sjs_concurrent_QueueExecutionContext$TimeoutsExecutionContext = new $TypeData().i($c_sjs_concurrent_QueueExecutionContext$TimeoutsExecutionContext, "scala.scalajs.concurrent.QueueExecutionContext$TimeoutsExecutionContext", ({
  hZ: 1,
  aX: 1,
  aW: 1,
  aF: 1
}));
/** @constructor */
function $c_sjsr_AnonFunction0_$$Lambda$2bf0f8dc580d6edeb2d6a336c52a1bab3049702d(f) {
  this.mN = null;
  this.mN = f;
}
$p = $c_sjsr_AnonFunction0_$$Lambda$2bf0f8dc580d6edeb2d6a336c52a1bab3049702d.prototype = new $h_sjsr_AnonFunction0();
$p.constructor = $c_sjsr_AnonFunction0_$$Lambda$2bf0f8dc580d6edeb2d6a336c52a1bab3049702d;
/** @constructor */
function $h_sjsr_AnonFunction0_$$Lambda$2bf0f8dc580d6edeb2d6a336c52a1bab3049702d() {
}
$h_sjsr_AnonFunction0_$$Lambda$2bf0f8dc580d6edeb2d6a336c52a1bab3049702d.prototype = $p;
$p.F = (function() {
  return (0, this.mN)();
});
var $d_sjsr_AnonFunction0_$$Lambda$2bf0f8dc580d6edeb2d6a336c52a1bab3049702d = new $TypeData().i($c_sjsr_AnonFunction0_$$Lambda$2bf0f8dc580d6edeb2d6a336c52a1bab3049702d, "scala.scalajs.runtime.AnonFunction0.$$Lambda$2bf0f8dc580d6edeb2d6a336c52a1bab3049702d", ({
  i9: 1,
  i8: 1,
  cx: 1,
  aH: 1
}));
/** @constructor */
function $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(f) {
  this.mO = null;
  this.mO = f;
}
$p = $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1.prototype = new $h_sjsr_AnonFunction1();
$p.constructor = $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1;
/** @constructor */
function $h_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1() {
}
$h_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1.prototype = $p;
$p.b = (function(x0) {
  return (0, this.mO)(x0);
});
var $d_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1 = new $TypeData().i($c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1, "scala.scalajs.runtime.AnonFunction1.$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1", ({
  ib: 1,
  ia: 1,
  cy: 1,
  e: 1
}));
/** @constructor */
function $c_sjsr_AnonFunction2_$$Lambda$770e9b86e03b055b1d78d82135c9f39ea48d32d7(f) {
  this.mP = null;
  this.mP = f;
}
$p = $c_sjsr_AnonFunction2_$$Lambda$770e9b86e03b055b1d78d82135c9f39ea48d32d7.prototype = new $h_sjsr_AnonFunction2();
$p.constructor = $c_sjsr_AnonFunction2_$$Lambda$770e9b86e03b055b1d78d82135c9f39ea48d32d7;
/** @constructor */
function $h_sjsr_AnonFunction2_$$Lambda$770e9b86e03b055b1d78d82135c9f39ea48d32d7() {
}
$h_sjsr_AnonFunction2_$$Lambda$770e9b86e03b055b1d78d82135c9f39ea48d32d7.prototype = $p;
$p.eM = (function(x0, x1) {
  return (0, this.mP)(x0, x1);
});
var $d_sjsr_AnonFunction2_$$Lambda$770e9b86e03b055b1d78d82135c9f39ea48d32d7 = new $TypeData().i($c_sjsr_AnonFunction2_$$Lambda$770e9b86e03b055b1d78d82135c9f39ea48d32d7, "scala.scalajs.runtime.AnonFunction2.$$Lambda$770e9b86e03b055b1d78d82135c9f39ea48d32d7", ({
  id: 1,
  ic: 1,
  cz: 1,
  aI: 1
}));
/** @constructor */
function $c_sjsr_AnonFunction3_$$Lambda$73f37e31ba038fe839c174212837da323f140c96(f) {
  this.mQ = null;
  this.mQ = f;
}
$p = $c_sjsr_AnonFunction3_$$Lambda$73f37e31ba038fe839c174212837da323f140c96.prototype = new $h_sjsr_AnonFunction3();
$p.constructor = $c_sjsr_AnonFunction3_$$Lambda$73f37e31ba038fe839c174212837da323f140c96;
/** @constructor */
function $h_sjsr_AnonFunction3_$$Lambda$73f37e31ba038fe839c174212837da323f140c96() {
}
$h_sjsr_AnonFunction3_$$Lambda$73f37e31ba038fe839c174212837da323f140c96.prototype = $p;
$p.iI = (function(x0, x1, x2) {
  return (0, this.mQ)(x0, x1, x2);
});
var $d_sjsr_AnonFunction3_$$Lambda$73f37e31ba038fe839c174212837da323f140c96 = new $TypeData().i($c_sjsr_AnonFunction3_$$Lambda$73f37e31ba038fe839c174212837da323f140c96, "scala.scalajs.runtime.AnonFunction3.$$Lambda$73f37e31ba038fe839c174212837da323f140c96", ({
  ig: 1,
  ie: 1,
  hI: 1,
  f6: 1
}));
/** @constructor */
function $c_sjsr_AnonFunction4_$$Lambda$120c664e6fb20e1c3552e9e8baf775b7682c102c(f) {
  this.mR = null;
  this.mR = f;
}
$p = $c_sjsr_AnonFunction4_$$Lambda$120c664e6fb20e1c3552e9e8baf775b7682c102c.prototype = new $h_sjsr_AnonFunction4();
$p.constructor = $c_sjsr_AnonFunction4_$$Lambda$120c664e6fb20e1c3552e9e8baf775b7682c102c;
/** @constructor */
function $h_sjsr_AnonFunction4_$$Lambda$120c664e6fb20e1c3552e9e8baf775b7682c102c() {
}
$h_sjsr_AnonFunction4_$$Lambda$120c664e6fb20e1c3552e9e8baf775b7682c102c.prototype = $p;
$p.pb = (function(x0, x1, x2, x3) {
  return (0, this.mR)(x0, x1, x2, x3);
});
var $d_sjsr_AnonFunction4_$$Lambda$120c664e6fb20e1c3552e9e8baf775b7682c102c = new $TypeData().i($c_sjsr_AnonFunction4_$$Lambda$120c664e6fb20e1c3552e9e8baf775b7682c102c, "scala.scalajs.runtime.AnonFunction4.$$Lambda$120c664e6fb20e1c3552e9e8baf775b7682c102c", ({
  ii: 1,
  ih: 1,
  hJ: 1,
  f7: 1
}));
/** @constructor */
function $c_s_util_Try() {
}
$p = $c_s_util_Try.prototype = new $h_O();
$p.constructor = $c_s_util_Try;
/** @constructor */
function $h_s_util_Try() {
}
$h_s_util_Try.prototype = $p;
$p.bx = (function() {
  return new $c_s_Product$$anon$1(this);
});
function $isArrayOf_s_util_Try(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.b0)));
}
function $f_Lcom_raquo_airstream_core_WritableObservable__$init$__V($thiz) {
  $thiz.h1($m_Lcom_raquo_ew_JsArray$().bb($m_sr_ScalaRunTime$().b4(new ($d_Lcom_raquo_airstream_core_Observer.r().C)([]))));
  $thiz.h2($m_Lcom_raquo_ew_JsArray$().bb($m_sr_ScalaRunTime$().b4(new ($d_Lcom_raquo_airstream_core_InternalObserver.r().C)([]))));
  $thiz.f0(false);
}
function $f_Lcom_raquo_airstream_core_WritableObservable__addObserver__Lcom_raquo_airstream_core_Observer__Lcom_raquo_airstream_ownership_Owner__Lcom_raquo_airstream_ownership_Subscription($thiz, observer, owner) {
  var this$2 = $m_Lcom_raquo_airstream_core_Transaction$onStart$();
  var f = (() => {
    $f_Lcom_raquo_airstream_core_WritableObservable__maybeWillStart__V($thiz);
    var subscription = $f_Lcom_raquo_airstream_core_WritableObservable__addExternalObserver__Lcom_raquo_airstream_core_Observer__Lcom_raquo_airstream_ownership_Owner__Lcom_raquo_airstream_ownership_Subscription($thiz, observer, owner);
    $thiz.hd(observer);
    $p_Lcom_raquo_airstream_core_WritableObservable__maybeStart__V($thiz);
    return subscription;
  });
  var when = (!$f_Lcom_raquo_airstream_core_BaseObservable__isStarted__Z($thiz));
  if ((this$2.aY || (!when))) {
    var $x_1 = f();
  } else {
    this$2.aY = true;
    try {
      var $x_1 = f();
    } finally {
      this$2.aY = false;
      $p_Lcom_raquo_airstream_core_Transaction$onStart$__resolve__V(this$2);
    }
  }
  return $x_1;
}
function $f_Lcom_raquo_airstream_core_WritableObservable__addExternalObserver__Lcom_raquo_airstream_core_Observer__Lcom_raquo_airstream_ownership_Owner__Lcom_raquo_airstream_ownership_Subscription($thiz, observer, owner) {
  var subscription = new $c_Lcom_raquo_airstream_ownership_Subscription(owner, new $c_sjsr_AnonFunction0_$$Lambda$2bf0f8dc580d6edeb2d6a336c52a1bab3049702d((() => {
    $f_Lcom_raquo_airstream_core_BaseObservable__removeExternalObserver__Lcom_raquo_airstream_core_Observer__V($thiz, observer);
  })));
  var this$ = $thiz.cV();
  this$.push(observer);
  return subscription;
}
function $f_Lcom_raquo_airstream_core_WritableObservable__addInternalObserver__Lcom_raquo_airstream_core_InternalObserver__Z__V($thiz, observer, shouldCallMaybeWillStart) {
  var this$3 = $m_Lcom_raquo_airstream_core_Transaction$onStart$();
  var f = (() => {
    if (((!$f_Lcom_raquo_airstream_core_BaseObservable__isStarted__Z($thiz)) && shouldCallMaybeWillStart)) {
      $f_Lcom_raquo_airstream_core_WritableObservable__maybeWillStart__V($thiz);
    }
    var this$ = $thiz.cX();
    this$.push(observer);
    $p_Lcom_raquo_airstream_core_WritableObservable__maybeStart__V($thiz);
  });
  var when = (!$f_Lcom_raquo_airstream_core_BaseObservable__isStarted__Z($thiz));
  if ((this$3.aY || (!when))) {
    f();
  } else {
    this$3.aY = true;
    try {
      f();
    } finally {
      this$3.aY = false;
      $p_Lcom_raquo_airstream_core_Transaction$onStart$__resolve__V(this$3);
    }
  }
}
function $f_Lcom_raquo_airstream_core_WritableObservable__removeInternalObserverNow__Lcom_raquo_airstream_core_InternalObserver__V($thiz, observer) {
  if ($m_Lcom_raquo_airstream_core_ObserverList$().o3($thiz.cX(), observer)) {
    $p_Lcom_raquo_airstream_core_WritableObservable__maybeStop__V($thiz);
  }
}
function $f_Lcom_raquo_airstream_core_WritableObservable__removeExternalObserverNow__Lcom_raquo_airstream_core_Observer__V($thiz, observer) {
  if ($m_Lcom_raquo_airstream_core_ObserverList$().o3($thiz.cV(), observer)) {
    $p_Lcom_raquo_airstream_core_WritableObservable__maybeStop__V($thiz);
  }
}
function $f_Lcom_raquo_airstream_core_WritableObservable__maybeWillStart__V($thiz) {
  if ((!$thiz.ho())) {
    $thiz.hi();
    $thiz.f0(true);
  }
}
function $p_Lcom_raquo_airstream_core_WritableObservable__maybeStart__V($thiz) {
  if (($f_Lcom_raquo_airstream_core_WritableObservable__numAllObservers__I($thiz) === 1)) {
    $thiz.hf();
  }
}
function $p_Lcom_raquo_airstream_core_WritableObservable__maybeStop__V($thiz) {
  if ((!$f_Lcom_raquo_airstream_core_BaseObservable__isStarted__Z($thiz))) {
    $thiz.hg();
    $thiz.f0(false);
  }
}
function $f_Lcom_raquo_airstream_core_WritableObservable__numAllObservers__I($thiz) {
  var this$ = $thiz.cV();
  var $x_1 = this$.length;
  var this$$1 = $thiz.cX();
  return ((($x_1 | 0) + (this$$1.length | 0)) | 0);
}
/** @constructor */
function $c_Lcom_raquo_airstream_custom_CustomSource$$anon$1(outer) {
  this.jF = null;
  if ((outer === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
  this.jF = outer;
}
$p = $c_Lcom_raquo_airstream_custom_CustomSource$$anon$1.prototype = new $h_sr_AbstractPartialFunction();
$p.constructor = $c_Lcom_raquo_airstream_custom_CustomSource$$anon$1;
/** @constructor */
function $h_Lcom_raquo_airstream_custom_CustomSource$$anon$1() {
}
$h_Lcom_raquo_airstream_custom_CustomSource$$anon$1.prototype = $p;
$p.qu = (function(x) {
  return ((x !== null) || false);
});
$p.pg = (function(x, default$1) {
  return ((x !== null) ? (new $c_Lcom_raquo_airstream_core_Transaction(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((_$1) => {
    $f_Lcom_raquo_airstream_core_WritableStream__fireError__jl_Throwable__Lcom_raquo_airstream_core_Transaction__V(this.jF, x, _$1);
  }))), (void 0)) : default$1.b(x));
});
$p.ca = (function(x) {
  return this.qu(x);
});
$p.bX = (function(x, default$1) {
  return this.pg(x, default$1);
});
var $d_Lcom_raquo_airstream_custom_CustomSource$$anon$1 = new $TypeData().i($c_Lcom_raquo_airstream_custom_CustomSource$$anon$1, "com.raquo.airstream.custom.CustomSource$$anon$1", ({
  cT: 1,
  aZ: 1,
  e: 1,
  j: 1,
  a: 1
}));
function $f_Lcom_raquo_airstream_state_Var__$init$__V($thiz) {
  $thiz.ke = $m_Lcom_raquo_airstream_core_Observer$().q7(new $c_Lcom_raquo_airstream_state_Var$$anon$1($thiz), ($m_Lcom_raquo_airstream_core_Observer$(), true));
}
function $f_Lcom_raquo_airstream_state_Var__set__O__V($thiz, value) {
  var tryValue = new $c_s_util_Success(value);
  $thiz.ke.e5(tryValue);
}
function $f_Lcom_raquo_airstream_state_Var__update__F1__V($thiz, mod) {
  new $c_Lcom_raquo_airstream_core_Transaction(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((trx) => {
    matchResult12: {
      var x36 = $f_Lcom_raquo_airstream_core_WritableSignal__tryNow__s_util_Try($thiz.c3);
      if ((x36 instanceof $c_s_util_Success)) {
        var currentValue = x36.cn;
        try {
          var $x_1 = new $c_s_util_Success(mod.b(currentValue));
        } catch (e) {
          var e$2 = ((e instanceof $c_jl_Throwable) ? e : new $c_sjs_js_JavaScriptException(e));
          matchResult1: {
            var $x_1;
            var x2 = $m_s_util_control_NonFatal$().dF(e$2);
            if ((!x2.c())) {
              var $x_1 = new $c_s_util_Failure(x2.s());
              break matchResult1;
            }
            throw ((e$2 instanceof $c_sjs_js_JavaScriptException) ? e$2.K : e$2);
          }
        }
        $thiz.oc($x_1, trx);
        break matchResult12;
      }
      if ((x36 instanceof $c_s_util_Failure)) {
        var err = x36.c7;
        $m_Lcom_raquo_airstream_core_AirstreamError$().c2(new $c_Lcom_raquo_airstream_core_AirstreamError$VarError("Unable to update a failed Var. Consider Var#tryUpdate instead.", new $c_s_Some(err)));
        break matchResult12;
      }
      throw new $c_s_MatchError(x36);
    }
  })));
}
/** @constructor */
function $c_Lcom_raquo_airstream_state_Var$$anon$1(outer) {
  this.kf = null;
  if ((outer === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
  this.kf = outer;
}
$p = $c_Lcom_raquo_airstream_state_Var$$anon$1.prototype = new $h_sr_AbstractPartialFunction();
$p.constructor = $c_Lcom_raquo_airstream_state_Var$$anon$1;
/** @constructor */
function $h_Lcom_raquo_airstream_state_Var$$anon$1() {
}
$h_Lcom_raquo_airstream_state_Var$$anon$1.prototype = $p;
$p.qv = (function(x) {
  return true;
});
$p.ph = (function(x, default$1) {
  new $c_Lcom_raquo_airstream_core_Transaction(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((_$1) => {
    this.kf.oc(x, _$1);
  })));
});
$p.ca = (function(x) {
  return this.qv(x);
});
$p.bX = (function(x, default$1) {
  return this.ph(x, default$1);
});
var $d_Lcom_raquo_airstream_state_Var$$anon$1 = new $TypeData().i($c_Lcom_raquo_airstream_state_Var$$anon$1, "com.raquo.airstream.state.Var$$anon$1", ({
  d9: 1,
  aZ: 1,
  e: 1,
  j: 1,
  a: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_DomApi$$anon$2(outer) {
  if ((outer === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
}
$p = $c_Lcom_raquo_laminar_DomApi$$anon$2.prototype = new $h_sr_AbstractPartialFunction();
$p.constructor = $c_Lcom_raquo_laminar_DomApi$$anon$2;
/** @constructor */
function $h_Lcom_raquo_laminar_DomApi$$anon$2() {
}
$h_Lcom_raquo_laminar_DomApi$$anon$2.prototype = $p;
$p.ca = (function(x) {
  return (((typeof x) === "string") || false);
});
$p.bX = (function(x, default$1) {
  return (((typeof x) === "string") ? x : default$1.b(x));
});
var $d_Lcom_raquo_laminar_DomApi$$anon$2 = new $TypeData().i($c_Lcom_raquo_laminar_DomApi$$anon$2, "com.raquo.laminar.DomApi$$anon$2", ({
  df: 1,
  aZ: 1,
  e: 1,
  j: 1,
  a: 1
}));
function $f_Lcom_raquo_laminar_nodes_ReactiveElement__$init$__V($thiz) {
  $thiz.hX = new $c_Lcom_raquo_airstream_ownership_TransferableSubscription(new $c_sjsr_AnonFunction0_$$Lambda$2bf0f8dc580d6edeb2d6a336c52a1bab3049702d((() => {
    $thiz.c4.mX();
  })), new $c_sjsr_AnonFunction0_$$Lambda$2bf0f8dc580d6edeb2d6a336c52a1bab3049702d((() => {
    $thiz.c4.pF();
  })));
  $thiz.dM = (void 0);
  $thiz.fc = $m_sci_Map$EmptyMap$();
}
function $f_Lcom_raquo_laminar_nodes_ReactiveElement__addEventListener__Lcom_raquo_laminar_modifiers_EventListener__Z__V($thiz, listener, unsafePrepend) {
  if (($thiz.dM === (void 0))) {
    $thiz.dM = $m_Lcom_raquo_ew_JsArray$().bb($m_sr_ScalaRunTime$().b4(new ($d_Lcom_raquo_laminar_modifiers_EventListener.r().C)([listener])));
  } else if (unsafePrepend) {
    var x$1 = $thiz.dM;
    if ((x$1 === (void 0))) {
      var $x_1;
      throw $ct_ju_NoSuchElementException__T__(new $c_ju_NoSuchElementException(), "undefined.get");
    } else {
      var $x_1 = x$1;
    }
    $x_1.unshift(listener);
  } else {
    var x$2 = $thiz.dM;
    if ((x$2 === (void 0))) {
      var $x_2;
      throw $ct_ju_NoSuchElementException__T__(new $c_ju_NoSuchElementException(), "undefined.get");
    } else {
      var $x_2 = x$2;
    }
    $x_2.push(listener);
  }
}
function $f_Lcom_raquo_laminar_nodes_ReactiveElement__removeEventListener__I__V($thiz, index) {
  var x = $thiz.dM;
  if ((x !== (void 0))) {
    x.splice(index, 1);
  }
}
function $f_Lcom_raquo_laminar_nodes_ReactiveElement__indexOfEventListener__Lcom_raquo_laminar_modifiers_EventListener__I($thiz, listener) {
  var x = $thiz.dM;
  if ((x === (void 0))) {
    return (-1);
  } else {
    var found = false;
    var ix = 0;
    while (((!found) && (ix < (x.length | 0)))) {
      var x$1 = x[ix];
      if (((x$1 === null) ? (listener === null) : $dp_equals__O__Z(x$1, listener))) {
        found = true;
      } else {
        ix = ((1 + ix) | 0);
      }
    }
    return (found ? ix : (-1));
  }
}
function $f_Lcom_raquo_laminar_nodes_ReactiveElement__updateCompositeValue__Lcom_raquo_laminar_keys_CompositeKey__Lcom_raquo_laminar_modifiers_Modifier__sci_List__sci_List__V($thiz, key, reason, addItems, removeItems) {
  var keyItemsWithReason = $thiz.fc.c9(key, new $c_sjsr_AnonFunction0_$$Lambda$2bf0f8dc580d6edeb2d6a336c52a1bab3049702d((() => $m_sci_Nil$())));
  var f = ((item) => {
    var these = keyItemsWithReason;
    while ((!these.c())) {
      var x0 = these.n();
      var x = x0.aZ;
      if (((x === null) ? (item === null) : $dp_equals__O__Z(x, item))) {
        var x$3 = x0.aQ;
        if ((!((x$3 === null) ? (reason === null) : $dp_equals__O__Z(x$3, reason)))) {
          var $x_1 = true;
        } else {
          var $x_1 = (reason === null);
        }
      } else {
        var $x_1 = false;
      }
      if ($x_1) {
        return true;
      }
      these = these.l();
    }
    return false;
  });
  var itemsToAdd = $f_sc_SeqOps__distinct__O(addItems);
  _return$1: {
    var result;
    var l$tailLocal1 = removeItems;
    while (true) {
      if (l$tailLocal1.c()) {
        var result = $m_sci_Nil$();
        break;
      } else {
        var h = l$tailLocal1.n();
        var t = l$tailLocal1.l();
        if ((!(!f(h)))) {
          l$tailLocal1 = t;
          continue;
        }
        var start = l$tailLocal1;
        var remaining$tailLocal1 = t;
        while (true) {
          if (remaining$tailLocal1.c()) {
            var result = start;
            break _return$1;
          } else {
            var x$1 = remaining$tailLocal1.n();
            if ((!(!(!f(x$1))))) {
              remaining$tailLocal1 = remaining$tailLocal1.l();
              continue;
            }
            var firstMiss = remaining$tailLocal1;
            var newHead = new $c_sci_$colon$colon(start.n(), $m_sci_Nil$());
            var toProcess = start.l();
            var currentLast = newHead;
            while ((toProcess !== firstMiss)) {
              var newElem = new $c_sci_$colon$colon(toProcess.n(), $m_sci_Nil$());
              currentLast.J = newElem;
              currentLast = newElem;
              toProcess = toProcess.l();
            }
            var next = firstMiss.l();
            var nextToCopy = next;
            while ((!next.c())) {
              var head = next.n();
              if ((!(!(!f(head))))) {
                next = next.l();
              } else {
                while ((nextToCopy !== next)) {
                  var newElem$2 = new $c_sci_$colon$colon(nextToCopy.n(), $m_sci_Nil$());
                  currentLast.J = newElem$2;
                  currentLast = newElem$2;
                  nextToCopy = nextToCopy.l();
                }
                nextToCopy = next.l();
                next = next.l();
              }
            }
            if ((!nextToCopy.c())) {
              currentLast.J = nextToCopy;
            }
            var result = newHead;
            break _return$1;
          }
        }
      }
    }
  }
  var this$1 = $thiz.fc.c9(key, new $c_sjsr_AnonFunction0_$$Lambda$2bf0f8dc580d6edeb2d6a336c52a1bab3049702d((() => $m_sci_Nil$())));
  var f$1 = ((t$1) => result.bl(t$1.aZ));
  _return$3: {
    var $x_3;
    var l$tailLocal1$1 = this$1;
    while (true) {
      if (l$tailLocal1$1.c()) {
        var $x_3 = $m_sci_Nil$();
        break;
      } else {
        var h$1 = l$tailLocal1$1.n();
        var t$2 = l$tailLocal1$1.l();
        if ((!(!f$1(h$1)))) {
          l$tailLocal1$1 = t$2;
          continue;
        }
        var start$1 = l$tailLocal1$1;
        var remaining$tailLocal1$1 = t$2;
        while (true) {
          if (remaining$tailLocal1$1.c()) {
            var $x_3 = start$1;
            break _return$3;
          } else {
            var x$2 = remaining$tailLocal1$1.n();
            if ((!(!(!f$1(x$2))))) {
              remaining$tailLocal1$1 = remaining$tailLocal1$1.l();
              continue;
            }
            var firstMiss$1 = remaining$tailLocal1$1;
            var newHead$1 = new $c_sci_$colon$colon(start$1.n(), $m_sci_Nil$());
            var toProcess$1 = start$1.l();
            var currentLast$1 = newHead$1;
            while ((toProcess$1 !== firstMiss$1)) {
              var newElem$1 = new $c_sci_$colon$colon(toProcess$1.n(), $m_sci_Nil$());
              currentLast$1.J = newElem$1;
              currentLast$1 = newElem$1;
              toProcess$1 = toProcess$1.l();
            }
            var next$1 = firstMiss$1.l();
            var nextToCopy$1 = next$1;
            while ((!next$1.c())) {
              var head$1 = next$1.n();
              if ((!(!(!f$1(head$1))))) {
                next$1 = next$1.l();
              } else {
                while ((nextToCopy$1 !== next$1)) {
                  var newElem$2$1 = new $c_sci_$colon$colon(nextToCopy$1.n(), $m_sci_Nil$());
                  currentLast$1.J = newElem$2$1;
                  currentLast$1 = newElem$2$1;
                  nextToCopy$1 = nextToCopy$1.l();
                }
                nextToCopy$1 = next$1.l();
                next$1 = next$1.l();
              }
            }
            if ((!nextToCopy$1.c())) {
              currentLast$1.J = nextToCopy$1;
            }
            var $x_3 = newHead$1;
            break _return$3;
          }
        }
      }
    }
  }
  var f$2 = ((_$2) => new $c_T2(_$2, reason));
  if ((itemsToAdd === $m_sci_Nil$())) {
    var $x_2 = $m_sci_Nil$();
  } else {
    var x0$1 = itemsToAdd.n();
    var h$2 = new $c_sci_$colon$colon(f$2(x0$1), $m_sci_Nil$());
    var t$3 = h$2;
    var rest = itemsToAdd.l();
    while ((rest !== $m_sci_Nil$())) {
      var x0$2 = rest.n();
      var nx = new $c_sci_$colon$colon(f$2(x0$2), $m_sci_Nil$());
      t$3.J = nx;
      t$3 = nx;
      rest = rest.l();
    }
    var $x_2 = h$2;
  }
  var newItems = $x_3.n6($x_2);
  var domValues = key.hJ.nk(key.lv.b($thiz));
  var f$3 = ((elem) => result.bl(elem));
  _return$5: {
    var $x_5;
    var l$tailLocal1$2 = domValues;
    while (true) {
      if (l$tailLocal1$2.c()) {
        var $x_5 = $m_sci_Nil$();
        break;
      } else {
        var h$3 = l$tailLocal1$2.n();
        var t$4 = l$tailLocal1$2.l();
        if ((!(!f$3(h$3)))) {
          l$tailLocal1$2 = t$4;
          continue;
        }
        var start$2 = l$tailLocal1$2;
        var remaining$tailLocal1$2 = t$4;
        while (true) {
          if (remaining$tailLocal1$2.c()) {
            var $x_5 = start$2;
            break _return$5;
          } else {
            var x$4 = remaining$tailLocal1$2.n();
            if ((!(!(!f$3(x$4))))) {
              remaining$tailLocal1$2 = remaining$tailLocal1$2.l();
              continue;
            }
            var firstMiss$2 = remaining$tailLocal1$2;
            var newHead$2 = new $c_sci_$colon$colon(start$2.n(), $m_sci_Nil$());
            var toProcess$2 = start$2.l();
            var currentLast$2 = newHead$2;
            while ((toProcess$2 !== firstMiss$2)) {
              var newElem$3 = new $c_sci_$colon$colon(toProcess$2.n(), $m_sci_Nil$());
              currentLast$2.J = newElem$3;
              currentLast$2 = newElem$3;
              toProcess$2 = toProcess$2.l();
            }
            var next$2 = firstMiss$2.l();
            var nextToCopy$2 = next$2;
            while ((!next$2.c())) {
              var head$2 = next$2.n();
              if ((!(!(!f$3(head$2))))) {
                next$2 = next$2.l();
              } else {
                while ((nextToCopy$2 !== next$2)) {
                  var newElem$2$2 = new $c_sci_$colon$colon(nextToCopy$2.n(), $m_sci_Nil$());
                  currentLast$2.J = newElem$2$2;
                  currentLast$2 = newElem$2$2;
                  nextToCopy$2 = nextToCopy$2.l();
                }
                nextToCopy$2 = next$2.l();
                next$2 = next$2.l();
              }
            }
            if ((!nextToCopy$2.c())) {
              currentLast$2.J = nextToCopy$2;
            }
            var $x_5 = newHead$2;
            break _return$5;
          }
        }
      }
    }
  }
  _return$7: {
    var $x_4;
    var l$tailLocal1$3 = itemsToAdd;
    while (true) {
      if (l$tailLocal1$3.c()) {
        var $x_4 = $m_sci_Nil$();
        break;
      } else {
        var h$4 = l$tailLocal1$3.n();
        var t$5 = l$tailLocal1$3.l();
        if ((!(!f(h$4)))) {
          l$tailLocal1$3 = t$5;
          continue;
        }
        var start$3 = l$tailLocal1$3;
        var remaining$tailLocal1$3 = t$5;
        while (true) {
          if (remaining$tailLocal1$3.c()) {
            var $x_4 = start$3;
            break _return$7;
          } else {
            var x$5 = remaining$tailLocal1$3.n();
            if ((!(!(!f(x$5))))) {
              remaining$tailLocal1$3 = remaining$tailLocal1$3.l();
              continue;
            }
            var firstMiss$3 = remaining$tailLocal1$3;
            var newHead$3 = new $c_sci_$colon$colon(start$3.n(), $m_sci_Nil$());
            var toProcess$3 = start$3.l();
            var currentLast$3 = newHead$3;
            while ((toProcess$3 !== firstMiss$3)) {
              var newElem$4 = new $c_sci_$colon$colon(toProcess$3.n(), $m_sci_Nil$());
              currentLast$3.J = newElem$4;
              currentLast$3 = newElem$4;
              toProcess$3 = toProcess$3.l();
            }
            var next$3 = firstMiss$3.l();
            var nextToCopy$3 = next$3;
            while ((!next$3.c())) {
              var head$3 = next$3.n();
              if ((!(!(!f(head$3))))) {
                next$3 = next$3.l();
              } else {
                while ((nextToCopy$3 !== next$3)) {
                  var newElem$2$3 = new $c_sci_$colon$colon(nextToCopy$3.n(), $m_sci_Nil$());
                  currentLast$3.J = newElem$2$3;
                  currentLast$3 = newElem$2$3;
                  nextToCopy$3 = nextToCopy$3.l();
                }
                nextToCopy$3 = next$3.l();
                next$3 = next$3.l();
              }
            }
            if ((!nextToCopy$3.c())) {
              currentLast$3.J = nextToCopy$3;
            }
            var $x_4 = newHead$3;
            break _return$7;
          }
        }
      }
    }
  }
  var nextDomValues = $x_5.n6($x_4);
  $thiz.fc = $thiz.fc.cd(key, newItems);
  key.lx.eM($thiz, key.hJ.nn(nextDomValues));
}
function $f_Lcom_raquo_laminar_nodes_ReactiveElement__willSetParent__s_Option__V($thiz, maybeNextParent) {
  if ($p_Lcom_raquo_laminar_nodes_ReactiveElement__isUnmounting__s_Option__s_Option__Z($thiz, $thiz.fb, maybeNextParent)) {
    $p_Lcom_raquo_laminar_nodes_ReactiveElement__setPilotSubscriptionOwner__s_Option__V($thiz, maybeNextParent);
  }
}
function $f_Lcom_raquo_laminar_nodes_ReactiveElement__setParent__s_Option__V($thiz, maybeNextParent) {
  var maybePrevParent = $thiz.fb;
  $thiz.fb = maybeNextParent;
  if ((!$p_Lcom_raquo_laminar_nodes_ReactiveElement__isUnmounting__s_Option__s_Option__Z($thiz, maybePrevParent, maybeNextParent))) {
    $p_Lcom_raquo_laminar_nodes_ReactiveElement__setPilotSubscriptionOwner__s_Option__V($thiz, maybeNextParent);
  }
}
function $p_Lcom_raquo_laminar_nodes_ReactiveElement__isUnmounting__s_Option__s_Option__Z($thiz, maybePrevParent, maybeNextParent) {
  var isPrevParentActive = ((!maybePrevParent.c()) && (!maybePrevParent.s().h3().bz.c()));
  var isNextParentActive = ((!maybeNextParent.c()) && (!maybeNextParent.s().h3().bz.c()));
  return (isPrevParentActive && (!isNextParentActive));
}
function $p_Lcom_raquo_laminar_nodes_ReactiveElement__setPilotSubscriptionOwner__s_Option__V($thiz, maybeNextParent) {
  $f_Lcom_raquo_laminar_nodes_ReactiveElement__unsafeSetPilotSubscriptionOwner__s_Option__V($thiz, (maybeNextParent.c() ? $m_s_None$() : new $c_s_Some(maybeNextParent.s().h3())));
}
function $f_Lcom_raquo_laminar_nodes_ReactiveElement__unsafeSetPilotSubscriptionOwner__s_Option__V($thiz, maybeNextOwner) {
  if (maybeNextOwner.c()) {
    $thiz.hX.ps();
  } else {
    var x0 = maybeNextOwner.s();
    $thiz.hX.rc(x0);
  }
}
function $ct_Ljava_io_FilterOutputStream__Ljava_io_OutputStream__($thiz, out) {
  return $thiz;
}
/** @constructor */
function $c_Ljava_io_FilterOutputStream() {
}
$p = $c_Ljava_io_FilterOutputStream.prototype = new $h_Ljava_io_OutputStream();
$p.constructor = $c_Ljava_io_FilterOutputStream;
/** @constructor */
function $h_Ljava_io_FilterOutputStream() {
}
$h_Ljava_io_FilterOutputStream.prototype = $p;
class $c_jl_ArithmeticException extends $c_jl_RuntimeException {
  constructor(s) {
    super();
    $ct_jl_Throwable__T__jl_Throwable__Z__Z__(this, s, null, true, true);
  }
}
var $d_jl_ArithmeticException = new $TypeData().i($c_jl_ArithmeticException, "java.lang.ArithmeticException", ({
  ev: 1,
  D: 1,
  B: 1,
  s: 1,
  a: 1
}));
function $f_jl_Byte__equals__O__Z($thiz, that) {
  return Object.is($thiz, that);
}
function $f_jl_Byte__hashCode__I($thiz) {
  return $thiz;
}
function $f_jl_Byte__toString__T($thiz) {
  return ("" + $thiz);
}
var $d_jl_Byte = new $TypeData().i(0, "java.lang.Byte", ({
  ey: 1,
  a8: 1,
  a: 1,
  a1: 1,
  Y: 1
}), ((x) => $isByte(x)));
function $isArrayOf_jl_ClassCastException(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.eB)));
}
function $ct_jl_IllegalArgumentException__T__($thiz, s) {
  $ct_jl_Throwable__T__jl_Throwable__Z__Z__($thiz, s, null, true, true);
  return $thiz;
}
function $ct_jl_IllegalArgumentException__($thiz) {
  $ct_jl_Throwable__T__jl_Throwable__Z__Z__($thiz, null, null, true, true);
  return $thiz;
}
class $c_jl_IllegalArgumentException extends $c_jl_RuntimeException {
}
var $d_jl_IllegalArgumentException = new $TypeData().i($c_jl_IllegalArgumentException, "java.lang.IllegalArgumentException", ({
  bx: 1,
  D: 1,
  B: 1,
  s: 1,
  a: 1
}));
class $c_jl_IllegalStateException extends $c_jl_RuntimeException {
  constructor(s) {
    super();
    $ct_jl_Throwable__T__jl_Throwable__Z__Z__(this, s, null, true, true);
  }
}
var $d_jl_IllegalStateException = new $TypeData().i($c_jl_IllegalStateException, "java.lang.IllegalStateException", ({
  eD: 1,
  D: 1,
  B: 1,
  s: 1,
  a: 1
}));
function $ct_jl_IndexOutOfBoundsException__T__($thiz, s) {
  $ct_jl_Throwable__T__jl_Throwable__Z__Z__($thiz, s, null, true, true);
  return $thiz;
}
function $ct_jl_IndexOutOfBoundsException__I__($thiz, index) {
  $ct_jl_Throwable__T__jl_Throwable__Z__Z__($thiz, ("Index out of range: " + index), null, true, true);
  return $thiz;
}
class $c_jl_IndexOutOfBoundsException extends $c_jl_RuntimeException {
}
var $d_jl_IndexOutOfBoundsException = new $TypeData().i($c_jl_IndexOutOfBoundsException, "java.lang.IndexOutOfBoundsException", ({
  by: 1,
  D: 1,
  B: 1,
  s: 1,
  a: 1
}));
/** @constructor */
function $c_jl_JSConsoleBasedPrintStream$DummyOutputStream() {
}
$p = $c_jl_JSConsoleBasedPrintStream$DummyOutputStream.prototype = new $h_Ljava_io_OutputStream();
$p.constructor = $c_jl_JSConsoleBasedPrintStream$DummyOutputStream;
/** @constructor */
function $h_jl_JSConsoleBasedPrintStream$DummyOutputStream() {
}
$h_jl_JSConsoleBasedPrintStream$DummyOutputStream.prototype = $p;
var $d_jl_JSConsoleBasedPrintStream$DummyOutputStream = new $TypeData().i($c_jl_JSConsoleBasedPrintStream$DummyOutputStream, "java.lang.JSConsoleBasedPrintStream$DummyOutputStream", ({
  eI: 1,
  br: 1,
  bp: 1,
  bt: 1,
  bq: 1
}));
function $ct_jl_NullPointerException__T__($thiz, s) {
  $ct_jl_Throwable__T__jl_Throwable__Z__Z__($thiz, s, null, true, true);
  return $thiz;
}
function $ct_jl_NullPointerException__($thiz) {
  $ct_jl_Throwable__T__jl_Throwable__Z__Z__($thiz, null, null, true, true);
  return $thiz;
}
class $c_jl_NullPointerException extends $c_jl_RuntimeException {
}
var $d_jl_NullPointerException = new $TypeData().i($c_jl_NullPointerException, "java.lang.NullPointerException", ({
  eK: 1,
  D: 1,
  B: 1,
  s: 1,
  a: 1
}));
function $isArrayOf_jl_SecurityException(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.eM)));
}
function $f_jl_Short__equals__O__Z($thiz, that) {
  return Object.is($thiz, that);
}
function $f_jl_Short__hashCode__I($thiz) {
  return $thiz;
}
function $f_jl_Short__toString__T($thiz) {
  return ("" + $thiz);
}
var $d_jl_Short = new $TypeData().i(0, "java.lang.Short", ({
  eN: 1,
  a8: 1,
  a: 1,
  a1: 1,
  Y: 1
}), ((x) => $isShort(x)));
class $c_jl_StackOverflowError extends $c_jl_VirtualMachineError {
  constructor(s) {
    super();
    $ct_jl_Throwable__T__jl_Throwable__Z__Z__(this, s, null, true, true);
  }
}
var $d_jl_StackOverflowError = new $TypeData().i($c_jl_StackOverflowError, "java.lang.StackOverflowError", ({
  eO: 1,
  bC: 1,
  bw: 1,
  s: 1,
  a: 1
}));
class $c_jl_UnsupportedOperationException extends $c_jl_RuntimeException {
  constructor(s) {
    super();
    $ct_jl_Throwable__T__jl_Throwable__Z__Z__(this, s, null, true, true);
  }
}
var $d_jl_UnsupportedOperationException = new $TypeData().i($c_jl_UnsupportedOperationException, "java.lang.UnsupportedOperationException", ({
  eX: 1,
  D: 1,
  B: 1,
  s: 1,
  a: 1
}));
class $c_ju_ConcurrentModificationException extends $c_jl_RuntimeException {
  constructor(s) {
    super();
    $ct_jl_Throwable__T__jl_Throwable__Z__Z__(this, s, null, true, true);
  }
}
var $d_ju_ConcurrentModificationException = new $TypeData().i($c_ju_ConcurrentModificationException, "java.util.ConcurrentModificationException", ({
  f1: 1,
  D: 1,
  B: 1,
  s: 1,
  a: 1
}));
function $ct_ju_NoSuchElementException__T__($thiz, s) {
  $ct_jl_Throwable__T__jl_Throwable__Z__Z__($thiz, s, null, true, true);
  return $thiz;
}
class $c_ju_NoSuchElementException extends $c_jl_RuntimeException {
}
var $d_ju_NoSuchElementException = new $TypeData().i($c_ju_NoSuchElementException, "java.util.NoSuchElementException", ({
  at: 1,
  D: 1,
  B: 1,
  s: 1,
  a: 1
}));
function $p_s_MatchError__objString__T($thiz) {
  if ((!$thiz.lW)) {
    if (($thiz.gB === null)) {
      var $x_1 = "null";
    } else {
      var this$1 = $thiz.gB;
      var cls = $objectGetClass(this$1);
      var ofClass = ((cls === null) ? "of a JS class" : ("of class " + cls.ah.N));
      try {
        var $x_1 = ((($thiz.gB + " (") + ofClass) + ")");
      } catch (e) {
        var $x_1 = ("an instance " + ofClass);
      }
    }
    $thiz.lV = $x_1;
    $thiz.lW = true;
  }
  return $thiz.lV;
}
class $c_s_MatchError extends $c_jl_RuntimeException {
  constructor(obj) {
    super();
    this.gB = null;
    this.lV = null;
    this.lW = false;
    this.gB = obj;
    $ct_jl_Throwable__T__jl_Throwable__Z__Z__(this, null, null, true, true);
  }
  eS() {
    return $p_s_MatchError__objString__T(this);
  }
}
var $d_s_MatchError = new $TypeData().i($c_s_MatchError, "scala.MatchError", ({
  fa: 1,
  D: 1,
  B: 1,
  s: 1,
  a: 1
}));
/** @constructor */
function $c_s_Option() {
}
$p = $c_s_Option.prototype = new $h_O();
$p.constructor = $c_s_Option;
/** @constructor */
function $h_s_Option() {
}
$h_s_Option.prototype = $p;
$p.bx = (function() {
  return new $c_s_Product$$anon$1(this);
});
$p.c = (function() {
  return (this === $m_s_None$());
});
$p.x = (function() {
  return ((!this.c()) | 0);
});
$p.bl = (function(elem) {
  return ((!this.c()) && $m_sr_BoxesRunTime$().j(this.s(), elem));
});
$p.i = (function() {
  return (this.c() ? $m_sc_Iterator$().O : new $c_sc_Iterator$$anon$20(this.s()));
});
/** @constructor */
function $c_s_Product$$anon$1(outer) {
  this.fp = 0;
  this.lZ = 0;
  this.lY = null;
  if ((outer === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
  this.lY = outer;
  this.fp = 0;
  this.lZ = outer.aN();
}
$p = $c_s_Product$$anon$1.prototype = new $h_sc_AbstractIterator();
$p.constructor = $c_s_Product$$anon$1;
/** @constructor */
function $h_s_Product$$anon$1() {
}
$h_s_Product$$anon$1.prototype = $p;
$p.m = (function() {
  return (this.fp < this.lZ);
});
$p.g = (function() {
  var result = this.lY.aO(this.fp);
  this.fp = ((1 + this.fp) | 0);
  return result;
});
var $d_s_Product$$anon$1 = new $TypeData().i($c_s_Product$$anon$1, "scala.Product$$anon$1", ({
  fg: 1,
  t: 1,
  b: 1,
  c: 1,
  u: 1
}));
/** @constructor */
function $c_T2(_1, _2) {
  this.aZ = null;
  this.aQ = null;
  this.aZ = _1;
  this.aQ = _2;
}
$p = $c_T2.prototype = new $h_O();
$p.constructor = $c_T2;
/** @constructor */
function $h_T2() {
}
$h_T2.prototype = $p;
$p.aN = (function() {
  return 2;
});
$p.aO = (function(n) {
  return $f_s_Product2__productElement__I__O(this, n);
});
$p.t = (function() {
  return (((("(" + this.aZ) + ",") + this.aQ) + ")");
});
$p.aP = (function() {
  return "Tuple2";
});
$p.bx = (function() {
  return new $c_sr_ScalaRunTime$$anon$1(this);
});
$p.r = (function() {
  return $m_s_util_hashing_MurmurHash3$().e7(this, (-116390334), true);
});
$p.k = (function(x$1) {
  return ((this === x$1) || ((x$1 instanceof $c_T2) && ($m_sr_BoxesRunTime$().j(this.aZ, x$1.aZ) && $m_sr_BoxesRunTime$().j(this.aQ, x$1.aQ))));
});
function $isArrayOf_T2(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.bG)));
}
var $d_T2 = new $TypeData().i($c_T2, "scala.Tuple2", ({
  bG: 1,
  fh: 1,
  E: 1,
  d: 1,
  a: 1
}));
/** @constructor */
function $c_sc_ClassTagSeqFactory$AnySeqDelegate(delegate) {
  this.fr = null;
  $ct_sc_ClassTagIterableFactory$AnyIterableDelegate__sc_ClassTagIterableFactory__(this, delegate);
}
$p = $c_sc_ClassTagSeqFactory$AnySeqDelegate.prototype = new $h_sc_ClassTagIterableFactory$AnyIterableDelegate();
$p.constructor = $c_sc_ClassTagSeqFactory$AnySeqDelegate;
/** @constructor */
function $h_sc_ClassTagSeqFactory$AnySeqDelegate() {
}
$h_sc_ClassTagSeqFactory$AnySeqDelegate.prototype = $p;
var $d_sc_ClassTagSeqFactory$AnySeqDelegate = new $TypeData().i($c_sc_ClassTagSeqFactory$AnySeqDelegate, "scala.collection.ClassTagSeqFactory$AnySeqDelegate", ({
  fn: 1,
  fm: 1,
  a: 1,
  K: 1,
  a0: 1
}));
function $f_sc_Iterable__toString__T($thiz) {
  return $f_sc_IterableOnceOps__mkString__T__T__T__T($thiz, ($thiz.bZ() + "("), ", ", ")");
}
function $is_sc_Iterable(obj) {
  return (!(!((obj && obj.$classData) && obj.$classData.n.f)));
}
function $isArrayOf_sc_Iterable(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.f)));
}
/** @constructor */
function $c_sc_Iterator$$anon$19() {
}
$p = $c_sc_Iterator$$anon$19.prototype = new $h_sc_AbstractIterator();
$p.constructor = $c_sc_Iterator$$anon$19;
/** @constructor */
function $h_sc_Iterator$$anon$19() {
}
$h_sc_Iterator$$anon$19.prototype = $p;
$p.m = (function() {
  return false;
});
$p.qF = (function() {
  throw $ct_ju_NoSuchElementException__T__(new $c_ju_NoSuchElementException(), "next on empty iterator");
});
$p.x = (function() {
  return 0;
});
$p.g = (function() {
  this.qF();
});
$p.gg = (function(from, until) {
  return this;
});
var $d_sc_Iterator$$anon$19 = new $TypeData().i($c_sc_Iterator$$anon$19, "scala.collection.Iterator$$anon$19", ({
  fs: 1,
  t: 1,
  b: 1,
  c: 1,
  u: 1
}));
/** @constructor */
function $c_sc_Iterator$$anon$20(a$2) {
  this.m1 = null;
  this.fs = false;
  this.m1 = a$2;
  this.fs = false;
}
$p = $c_sc_Iterator$$anon$20.prototype = new $h_sc_AbstractIterator();
$p.constructor = $c_sc_Iterator$$anon$20;
/** @constructor */
function $h_sc_Iterator$$anon$20() {
}
$h_sc_Iterator$$anon$20.prototype = $p;
$p.m = (function() {
  return (!this.fs);
});
$p.g = (function() {
  if (this.fs) {
    return $m_sc_Iterator$().O.g();
  } else {
    this.fs = true;
    return this.m1;
  }
});
$p.gg = (function(from, until) {
  return (((this.fs || (from > 0)) || (until === 0)) ? $m_sc_Iterator$().O : this);
});
var $d_sc_Iterator$$anon$20 = new $TypeData().i($c_sc_Iterator$$anon$20, "scala.collection.Iterator$$anon$20", ({
  ft: 1,
  t: 1,
  b: 1,
  c: 1,
  u: 1
}));
/** @constructor */
function $c_sc_Iterator$$anon$8(f$8, outer) {
  this.m2 = null;
  this.m4 = null;
  this.gF = false;
  this.m3 = null;
  this.ie = null;
  this.m2 = f$8;
  if ((outer === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
  this.ie = outer;
  this.m4 = $ct_scm_HashSet__(new $c_scm_HashSet());
  this.gF = false;
}
$p = $c_sc_Iterator$$anon$8.prototype = new $h_sc_AbstractIterator();
$p.constructor = $c_sc_Iterator$$anon$8;
/** @constructor */
function $h_sc_Iterator$$anon$8() {
}
$h_sc_Iterator$$anon$8.prototype = $p;
$p.m = (function() {
  while (true) {
    if (this.gF) {
      return true;
    } else if (this.ie.m()) {
      var a = this.ie.g();
      if ((!this.m4.gV(this.m2.b(a)))) {
        continue;
      }
      this.m3 = a;
      this.gF = true;
      return true;
    } else {
      return false;
    }
  }
});
$p.g = (function() {
  if (this.m()) {
    this.gF = false;
    return this.m3;
  } else {
    return $m_sc_Iterator$().O.g();
  }
});
var $d_sc_Iterator$$anon$8 = new $TypeData().i($c_sc_Iterator$$anon$8, "scala.collection.Iterator$$anon$8", ({
  fv: 1,
  t: 1,
  b: 1,
  c: 1,
  u: 1
}));
/** @constructor */
function $c_sc_Iterator$$anon$9(f$9, outer) {
  this.m5 = null;
  this.gG = null;
  this.m5 = f$9;
  if ((outer === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
  this.gG = outer;
}
$p = $c_sc_Iterator$$anon$9.prototype = new $h_sc_AbstractIterator();
$p.constructor = $c_sc_Iterator$$anon$9;
/** @constructor */
function $h_sc_Iterator$$anon$9() {
}
$h_sc_Iterator$$anon$9.prototype = $p;
$p.x = (function() {
  return this.gG.x();
});
$p.m = (function() {
  return this.gG.m();
});
$p.g = (function() {
  return this.m5.b(this.gG.g());
});
var $d_sc_Iterator$$anon$9 = new $TypeData().i($c_sc_Iterator$$anon$9, "scala.collection.Iterator$$anon$9", ({
  fw: 1,
  t: 1,
  b: 1,
  c: 1,
  u: 1
}));
function $p_sc_Iterator$ConcatIterator__merge$1__V($thiz) {
  while (true) {
    if (($thiz.bs instanceof $c_sc_Iterator$ConcatIterator)) {
      var c = $thiz.bs;
      $thiz.bs = c.bs;
      $thiz.d3 = c.d3;
      if ((c.bM !== null)) {
        if (($thiz.bL === null)) {
          $thiz.bL = c.bL;
        }
        var x$proxy10 = c.bL;
        if ((x$proxy10 === null)) {
          $m_sr_Scala3RunTime$().bp();
        }
        x$proxy10.ft = $thiz.bM;
        $thiz.bM = c.bM;
      }
    } else {
      return (void 0);
    }
  }
}
function $p_sc_Iterator$ConcatIterator__advance$1__Z($thiz) {
  while (true) {
    if (($thiz.bM === null)) {
      $thiz.bs = null;
      $thiz.bL = null;
      return false;
    } else {
      $thiz.bs = $thiz.bM.qi();
      if (($thiz.bL === $thiz.bM)) {
        var x$proxy12 = $thiz.bL;
        if ((x$proxy12 === null)) {
          $m_sr_Scala3RunTime$().bp();
        }
        $thiz.bL = x$proxy12.ft;
      }
      $thiz.bM = $thiz.bM.ft;
      $p_sc_Iterator$ConcatIterator__merge$1__V($thiz);
      if ($thiz.d3) {
        return true;
      } else {
        if ((!(($thiz.bs !== null) && $thiz.bs.m()))) {
          continue;
        }
        $thiz.d3 = true;
        return true;
      }
    }
  }
}
/** @constructor */
function $c_sc_Iterator$ConcatIterator(from) {
  this.bs = null;
  this.bM = null;
  this.bL = null;
  this.d3 = false;
  this.bs = from;
  this.bM = null;
  this.bL = null;
  this.d3 = false;
}
$p = $c_sc_Iterator$ConcatIterator.prototype = new $h_sc_AbstractIterator();
$p.constructor = $c_sc_Iterator$ConcatIterator;
/** @constructor */
function $h_sc_Iterator$ConcatIterator() {
}
$h_sc_Iterator$ConcatIterator.prototype = $p;
$p.m = (function() {
  if (this.d3) {
    return true;
  } else if ((this.bs !== null)) {
    if (this.bs.m()) {
      this.d3 = true;
      return true;
    } else {
      return $p_sc_Iterator$ConcatIterator__advance$1__Z(this);
    }
  } else {
    return false;
  }
});
$p.g = (function() {
  if (this.m()) {
    this.d3 = false;
    var x$proxy13 = this.bs;
    if ((x$proxy13 === null)) {
      $m_sr_Scala3RunTime$().bp();
    }
    return x$proxy13.g();
  } else {
    return $m_sc_Iterator$().O.g();
  }
});
$p.iO = (function(that) {
  var c = new $c_sc_Iterator$ConcatIteratorCell(that, null);
  if ((this.bM === null)) {
    this.bM = c;
    this.bL = c;
  } else {
    var x$proxy14 = this.bL;
    if ((x$proxy14 === null)) {
      $m_sr_Scala3RunTime$().bp();
    }
    x$proxy14.ft = c;
    this.bL = c;
  }
  if ((this.bs === null)) {
    this.bs = $m_sc_Iterator$().O;
  }
  return this;
});
function $isArrayOf_sc_Iterator$ConcatIterator(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.bM)));
}
var $d_sc_Iterator$ConcatIterator = new $TypeData().i($c_sc_Iterator$ConcatIterator, "scala.collection.Iterator$ConcatIterator", ({
  bM: 1,
  t: 1,
  b: 1,
  c: 1,
  u: 1
}));
function $p_sc_Iterator$SliceIterator__skip__V($thiz) {
  while (($thiz.cF > 0)) {
    if ($thiz.d4.m()) {
      $thiz.d4.g();
      $thiz.cF = (($thiz.cF - 1) | 0);
    } else {
      $thiz.cF = 0;
    }
  }
}
function $p_sc_Iterator$SliceIterator__adjustedBound$1__I__I($thiz, lo$1) {
  if (($thiz.bA < 0)) {
    return (-1);
  } else {
    var that = (($thiz.bA - lo$1) | 0);
    return ((that < 0) ? 0 : that);
  }
}
/** @constructor */
function $c_sc_Iterator$SliceIterator(underlying, start, limit) {
  this.d4 = null;
  this.bA = 0;
  this.cF = 0;
  this.d4 = underlying;
  this.bA = limit;
  this.cF = start;
}
$p = $c_sc_Iterator$SliceIterator.prototype = new $h_sc_AbstractIterator();
$p.constructor = $c_sc_Iterator$SliceIterator;
/** @constructor */
function $h_sc_Iterator$SliceIterator() {
}
$h_sc_Iterator$SliceIterator.prototype = $p;
$p.x = (function() {
  var size = this.d4.x();
  if ((size < 0)) {
    return (-1);
  } else {
    var that = ((size - this.cF) | 0);
    var dropSize = ((that < 0) ? 0 : that);
    if ((this.bA < 0)) {
      return dropSize;
    } else {
      var x = this.bA;
      return ((x < dropSize) ? x : dropSize);
    }
  }
});
$p.m = (function() {
  $p_sc_Iterator$SliceIterator__skip__V(this);
  return ((this.bA !== 0) && this.d4.m());
});
$p.g = (function() {
  $p_sc_Iterator$SliceIterator__skip__V(this);
  if ((this.bA > 0)) {
    this.bA = ((this.bA - 1) | 0);
    return this.d4.g();
  } else {
    return ((this.bA < 0) ? this.d4.g() : $m_sc_Iterator$().O.g());
  }
});
$p.gg = (function(from, until) {
  var lo = ((from > 0) ? from : 0);
  if ((until < 0)) {
    var rest = $p_sc_Iterator$SliceIterator__adjustedBound$1__I__I(this, lo);
  } else if ((until <= lo)) {
    var rest = 0;
  } else if ((this.bA < 0)) {
    var rest = ((until - lo) | 0);
  } else {
    var x = $p_sc_Iterator$SliceIterator__adjustedBound$1__I__I(this, lo);
    var that = ((until - lo) | 0);
    var rest = ((x < that) ? x : that);
  }
  var sum = ((this.cF + lo) | 0);
  if ((rest === 0)) {
    return $m_sc_Iterator$().O;
  } else if ((sum < 0)) {
    this.cF = 2147483647;
    this.bA = 0;
    return $f_sc_Iterator__concat__F0__sc_Iterator(this, new $c_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c((() => new $c_sc_Iterator$SliceIterator(this.d4, ((sum - 2147483647) | 0), rest))));
  } else {
    this.cF = sum;
    this.bA = rest;
    return this;
  }
});
var $d_sc_Iterator$SliceIterator = new $TypeData().i($c_sc_Iterator$SliceIterator, "scala.collection.Iterator$SliceIterator", ({
  fy: 1,
  t: 1,
  b: 1,
  c: 1,
  u: 1
}));
function $f_sc_LinearSeqOps__length__I($thiz) {
  var these = $thiz;
  var len = 0;
  while ((!these.c())) {
    len = ((1 + len) | 0);
    these = these.l();
  }
  return len;
}
function $f_sc_LinearSeqOps__lengthCompare__I__I($thiz, len) {
  return ((len < 0) ? 1 : $p_sc_LinearSeqOps__loop$1__I__I__sc_LinearSeq__I($thiz, len, 0, $thiz));
}
function $f_sc_LinearSeqOps__isDefinedAt__I__Z($thiz, x) {
  return ((x >= 0) && ($thiz.bc(x) > 0));
}
function $f_sc_LinearSeqOps__apply__I__O($thiz, n) {
  if ((n < 0)) {
    throw $ct_jl_IndexOutOfBoundsException__T__(new $c_jl_IndexOutOfBoundsException(), ("" + n));
  }
  var skipped = $thiz.nm(n);
  if (skipped.c()) {
    throw $ct_jl_IndexOutOfBoundsException__T__(new $c_jl_IndexOutOfBoundsException(), ("" + n));
  }
  return skipped.n();
}
function $f_sc_LinearSeqOps__sameElements__sc_IterableOnce__Z($thiz, that) {
  return ($is_sc_LinearSeq(that) ? $p_sc_LinearSeqOps__linearSeqEq$1__sc_LinearSeq__sc_LinearSeq__Z($thiz, $thiz, that) : $f_sc_SeqOps__sameElements__sc_IterableOnce__Z($thiz, that));
}
function $p_sc_LinearSeqOps__loop$1__I__I__sc_LinearSeq__I($thiz, len$1, i, xs) {
  var xs$tailLocal1 = xs;
  var i$tailLocal1 = i;
  while (true) {
    if ((i$tailLocal1 === len$1)) {
      return ((!xs$tailLocal1.c()) | 0);
    } else {
      if ((!xs$tailLocal1.c())) {
        var i$tailLocal1$tmp1 = ((1 + i$tailLocal1) | 0);
        var xs$tailLocal1$tmp1 = xs$tailLocal1.l();
        i$tailLocal1 = i$tailLocal1$tmp1;
        xs$tailLocal1 = xs$tailLocal1$tmp1;
        continue;
      }
      return (-1);
    }
  }
}
function $p_sc_LinearSeqOps__linearSeqEq$1__sc_LinearSeq__sc_LinearSeq__Z($thiz, a, b) {
  var b$tailLocal1 = b;
  var a$tailLocal1 = a;
  while (true) {
    if ((a$tailLocal1 === b$tailLocal1)) {
      return true;
    } else {
      if ((((!a$tailLocal1.c()) && (!b$tailLocal1.c())) && $m_sr_BoxesRunTime$().j(a$tailLocal1.n(), b$tailLocal1.n()))) {
        var a$tailLocal1$tmp1 = a$tailLocal1.l();
        var b$tailLocal1$tmp1 = b$tailLocal1.l();
        a$tailLocal1 = a$tailLocal1$tmp1;
        b$tailLocal1 = b$tailLocal1$tmp1;
        continue;
      }
      return (a$tailLocal1.c() && b$tailLocal1.c());
    }
  }
}
/** @constructor */
function $c_sc_StrictOptimizedLinearSeqOps$$anon$1(outer) {
  this.fu = null;
  if ((outer === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
  this.fu = outer;
}
$p = $c_sc_StrictOptimizedLinearSeqOps$$anon$1.prototype = new $h_sc_AbstractIterator();
$p.constructor = $c_sc_StrictOptimizedLinearSeqOps$$anon$1;
/** @constructor */
function $h_sc_StrictOptimizedLinearSeqOps$$anon$1() {
}
$h_sc_StrictOptimizedLinearSeqOps$$anon$1.prototype = $p;
$p.m = (function() {
  return (!this.fu.c());
});
$p.g = (function() {
  var r = this.fu.n();
  this.fu = this.fu.l();
  return r;
});
var $d_sc_StrictOptimizedLinearSeqOps$$anon$1 = new $TypeData().i($c_sc_StrictOptimizedLinearSeqOps$$anon$1, "scala.collection.StrictOptimizedLinearSeqOps$$anon$1", ({
  fC: 1,
  t: 1,
  b: 1,
  c: 1,
  u: 1
}));
function $p_sc_StringOps$$anon$1__advance__T($thiz) {
  var start = $thiz.aD;
  while (true) {
    if (($thiz.aD < $thiz.dR)) {
      $m_sc_StringOps$();
      $m_sc_StringOps$();
      var this$ = $thiz.fv;
      var i = $thiz.aD;
      var c = this$.charCodeAt(i);
      var $x_1 = (!((c === 10) || (c === 13)));
    } else {
      var $x_1 = false;
    }
    if ($x_1) {
      $thiz.aD = ((1 + $thiz.aD) | 0);
    } else {
      break;
    }
  }
  var end = $thiz.aD;
  if (($thiz.aD < $thiz.dR)) {
    $m_sc_StringOps$();
    var this$$2 = $thiz.fv;
    var i$1 = $thiz.aD;
    var c$1 = this$$2.charCodeAt(i$1);
    $thiz.aD = ((1 + $thiz.aD) | 0);
    if ((($thiz.aD < $thiz.dR) && ($m_sc_StringOps$(), $m_sc_StringOps$(), (((13 ^ c$1) | (10 ^ $thiz.fv.charCodeAt($thiz.aD))) === 0)))) {
      $thiz.aD = ((1 + $thiz.aD) | 0);
    }
    if ((!$thiz.ma)) {
      end = $thiz.aD;
    }
  }
  var this$6 = $thiz.fv;
  var endIndex = end;
  return this$6.substring(start, endIndex);
}
/** @constructor */
function $c_sc_StringOps$$anon$1(\u03b4this$2, stripped$1) {
  this.fv = null;
  this.ma = false;
  this.dR = 0;
  this.aD = 0;
  this.fv = \u03b4this$2;
  this.ma = stripped$1;
  this.dR = \u03b4this$2.length;
  this.aD = 0;
}
$p = $c_sc_StringOps$$anon$1.prototype = new $h_sc_AbstractIterator();
$p.constructor = $c_sc_StringOps$$anon$1;
/** @constructor */
function $h_sc_StringOps$$anon$1() {
}
$h_sc_StringOps$$anon$1.prototype = $p;
$p.m = (function() {
  return (this.aD < this.dR);
});
$p.nR = (function() {
  return ((this.aD >= this.dR) ? $m_sc_Iterator$().O.g() : $p_sc_StringOps$$anon$1__advance__T(this));
});
$p.g = (function() {
  return this.nR();
});
var $d_sc_StringOps$$anon$1 = new $TypeData().i($c_sc_StringOps$$anon$1, "scala.collection.StringOps$$anon$1", ({
  fF: 1,
  t: 1,
  b: 1,
  c: 1,
  u: 1
}));
function $ct_sci_ChampBaseIterator__($thiz) {
  $thiz.bB = 0;
  $thiz.fw = 0;
  $thiz.bu = (-1);
  return $thiz;
}
function $p_sci_ChampBaseIterator__initNodes__V($thiz) {
  if (($thiz.cH === null)) {
    $thiz.cH = new $ac_I(($m_sci_Node$().fC << 1));
    $thiz.fx = new ($d_sci_Node.r().C)($m_sci_Node$().fC);
  }
}
function $ct_sci_ChampBaseIterator__sci_Node__($thiz, rootNode) {
  $ct_sci_ChampBaseIterator__($thiz);
  if (rootNode.j9()) {
    $p_sci_ChampBaseIterator__pushNode__sci_Node__V($thiz, rootNode);
  }
  if (rootNode.h9()) {
    $p_sci_ChampBaseIterator__setupPayloadNode__sci_Node__V($thiz, rootNode);
  }
  return $thiz;
}
function $p_sci_ChampBaseIterator__setupPayloadNode__sci_Node__V($thiz, node) {
  $thiz.dT = node;
  $thiz.bB = 0;
  $thiz.fw = node.jo();
}
function $p_sci_ChampBaseIterator__pushNode__sci_Node__V($thiz, node) {
  $p_sci_ChampBaseIterator__initNodes__V($thiz);
  $thiz.bu = ((1 + $thiz.bu) | 0);
  var cursorIndex = ($thiz.bu << 1);
  var lengthIndex = ((1 + ($thiz.bu << 1)) | 0);
  $thiz.fx.a[$thiz.bu] = node;
  $thiz.cH.a[cursorIndex] = 0;
  $thiz.cH.a[lengthIndex] = node.jj();
}
function $p_sci_ChampBaseIterator__popNode__V($thiz) {
  $thiz.bu = (($thiz.bu - 1) | 0);
}
function $p_sci_ChampBaseIterator__searchNextValueNode__Z($thiz) {
  while (($thiz.bu >= 0)) {
    var cursorIndex = ($thiz.bu << 1);
    var lengthIndex = ((1 + ($thiz.bu << 1)) | 0);
    var nodeCursor = $thiz.cH.a[cursorIndex];
    if ((nodeCursor < $thiz.cH.a[lengthIndex])) {
      var \u03b41$ = $thiz.cH;
      \u03b41$.a[cursorIndex] = ((1 + \u03b41$.a[cursorIndex]) | 0);
      var nextNode = $thiz.fx.a[$thiz.bu].j5(nodeCursor);
      if (nextNode.j9()) {
        $p_sci_ChampBaseIterator__pushNode__sci_Node__V($thiz, nextNode);
      }
      if (nextNode.h9()) {
        $p_sci_ChampBaseIterator__setupPayloadNode__sci_Node__V($thiz, nextNode);
        return true;
      }
    } else {
      $p_sci_ChampBaseIterator__popNode__V($thiz);
    }
  }
  return false;
}
/** @constructor */
function $c_sci_ChampBaseIterator() {
  this.bB = 0;
  this.fw = 0;
  this.dT = null;
  this.bu = 0;
  this.cH = null;
  this.fx = null;
}
$p = $c_sci_ChampBaseIterator.prototype = new $h_sc_AbstractIterator();
$p.constructor = $c_sci_ChampBaseIterator;
/** @constructor */
function $h_sci_ChampBaseIterator() {
}
$h_sci_ChampBaseIterator.prototype = $p;
$p.m = (function() {
  return ((this.bB < this.fw) || $p_sci_ChampBaseIterator__searchNextValueNode__Z(this));
});
function $ct_sci_ChampBaseReverseIterator__($thiz) {
  $thiz.dc = (-1);
  $thiz.bC = (-1);
  $thiz.fy = new $ac_I(((1 + $m_sci_Node$().fC) | 0));
  $thiz.fz = new ($d_sci_Node.r().C)(((1 + $m_sci_Node$().fC) | 0));
  return $thiz;
}
function $ct_sci_ChampBaseReverseIterator__sci_Node__($thiz, rootNode) {
  $ct_sci_ChampBaseReverseIterator__($thiz);
  $p_sci_ChampBaseReverseIterator__pushNode__sci_Node__V($thiz, rootNode);
  $p_sci_ChampBaseReverseIterator__searchNextValueNode__Z($thiz);
  return $thiz;
}
function $p_sci_ChampBaseReverseIterator__setupPayloadNode__sci_Node__V($thiz, node) {
  $thiz.gJ = node;
  $thiz.dc = ((node.jo() - 1) | 0);
}
function $p_sci_ChampBaseReverseIterator__pushNode__sci_Node__V($thiz, node) {
  $thiz.bC = ((1 + $thiz.bC) | 0);
  $thiz.fz.a[$thiz.bC] = node;
  $thiz.fy.a[$thiz.bC] = ((node.jj() - 1) | 0);
}
function $p_sci_ChampBaseReverseIterator__popNode__V($thiz) {
  $thiz.bC = (($thiz.bC - 1) | 0);
}
function $p_sci_ChampBaseReverseIterator__searchNextValueNode__Z($thiz) {
  while (($thiz.bC >= 0)) {
    var nodeCursor = $thiz.fy.a[$thiz.bC];
    $thiz.fy.a[$thiz.bC] = ((nodeCursor - 1) | 0);
    if ((nodeCursor >= 0)) {
      $p_sci_ChampBaseReverseIterator__pushNode__sci_Node__V($thiz, $thiz.fz.a[$thiz.bC].j5(nodeCursor));
    } else {
      var currNode = $thiz.fz.a[$thiz.bC];
      $p_sci_ChampBaseReverseIterator__popNode__V($thiz);
      if (currNode.h9()) {
        $p_sci_ChampBaseReverseIterator__setupPayloadNode__sci_Node__V($thiz, currNode);
        return true;
      }
    }
  }
  return false;
}
/** @constructor */
function $c_sci_ChampBaseReverseIterator() {
  this.dc = 0;
  this.gJ = null;
  this.bC = 0;
  this.fy = null;
  this.fz = null;
}
$p = $c_sci_ChampBaseReverseIterator.prototype = new $h_sc_AbstractIterator();
$p.constructor = $c_sci_ChampBaseReverseIterator;
/** @constructor */
function $h_sci_ChampBaseReverseIterator() {
}
$h_sci_ChampBaseReverseIterator.prototype = $p;
$p.m = (function() {
  return ((this.dc >= 0) || $p_sci_ChampBaseReverseIterator__searchNextValueNode__Z(this));
});
function $p_sci_HashMapBuilder__isAliased__Z($thiz) {
  return ($thiz.ex !== null);
}
function $p_sci_HashMapBuilder__insertElement__AI__I__I__AI($thiz, as, ix, elem) {
  if ((ix < 0)) {
    throw $ct_jl_ArrayIndexOutOfBoundsException__(new $c_jl_ArrayIndexOutOfBoundsException());
  }
  if ((ix > as.a.length)) {
    throw $ct_jl_ArrayIndexOutOfBoundsException__(new $c_jl_ArrayIndexOutOfBoundsException());
  }
  var result = new $ac_I(((1 + as.a.length) | 0));
  as.u(0, result, 0, ix);
  result.a[ix] = elem;
  var destPos = ((1 + ix) | 0);
  var length = ((as.a.length - ix) | 0);
  as.u(ix, result, destPos, length);
  return result;
}
function $p_sci_HashMapBuilder__insertValue__sci_BitmapIndexedMapNode__I__O__I__I__O__V($thiz, bm, bitpos, key, originalHash, keyHash, value) {
  var dataIx = bm.g0(bitpos);
  var idx = (dataIx << 1);
  var src = bm.ae;
  var dst = new $ac_O(((2 + src.a.length) | 0));
  src.u(0, dst, 0, idx);
  dst.a[idx] = key;
  dst.a[((1 + idx) | 0)] = value;
  var destPos = ((2 + idx) | 0);
  var length = ((src.a.length - idx) | 0);
  src.u(idx, dst, destPos, length);
  var dstHashes = $p_sci_HashMapBuilder__insertElement__AI__I__I__AI($thiz, bm.bt, dataIx, originalHash);
  bm.N = (bm.N | bitpos);
  bm.ae = dst;
  bm.bt = dstHashes;
  bm.aE = ((1 + bm.aE) | 0);
  bm.bd = ((bm.bd + keyHash) | 0);
}
function $p_sci_HashMapBuilder__ensureUnaliased__V($thiz) {
  if ($p_sci_HashMapBuilder__isAliased__Z($thiz)) {
    $p_sci_HashMapBuilder__copyElems__V($thiz);
  }
  $thiz.ex = null;
}
function $p_sci_HashMapBuilder__copyElems__V($thiz) {
  $thiz.cg = $thiz.cg.nh();
}
/** @constructor */
function $c_sci_HashMapBuilder() {
  this.ex = null;
  this.cg = null;
  this.cg = new $c_sci_BitmapIndexedMapNode(0, 0, $m_s_Array$EmptyArrays$().lU, $m_s_Array$EmptyArrays$().ic, 0, 0);
}
$p = $c_sci_HashMapBuilder.prototype = new $h_O();
$p.constructor = $c_sci_HashMapBuilder;
/** @constructor */
function $h_sci_HashMapBuilder() {
}
$h_sci_HashMapBuilder.prototype = $p;
$p.aX = (function(size) {
});
$p.eY = (function(mapNode, key, value, originalHash, keyHash, shift) {
  if ((mapNode instanceof $c_sci_BitmapIndexedMapNode)) {
    var mask = $m_sci_Node$().dE(keyHash, shift);
    var bitpos = $m_sci_Node$().cU(mask);
    if (((mapNode.N & bitpos) !== 0)) {
      var index = $m_sci_Node$().c1(mapNode.N, mask, bitpos);
      var key0 = mapNode.cW(index);
      var key0UnimprovedHash = mapNode.g3(index);
      if (((key0UnimprovedHash === originalHash) && $m_sr_BoxesRunTime$().j(key0, key))) {
        mapNode.ae.a[((1 + (index << 1)) | 0)] = value;
        return (void 0);
      } else {
        var value0 = mapNode.ct(index);
        var key0Hash = $m_sc_Hashing$().c0(key0UnimprovedHash);
        var subNodeNew = mapNode.ji(key0, value0, key0UnimprovedHash, key0Hash, key, value, originalHash, keyHash, ((5 + shift) | 0));
        mapNode.qB(bitpos, key0Hash, subNodeNew);
        return (void 0);
      }
    } else if (((mapNode.T & bitpos) !== 0)) {
      var index$2 = $m_sci_Node$().c1(mapNode.T, mask, bitpos);
      var subNode = mapNode.cs(index$2);
      var beforeSize = subNode.ax();
      var beforeHash = subNode.dB();
      this.eY(subNode, key, value, originalHash, keyHash, ((5 + shift) | 0));
      mapNode.aE = ((mapNode.aE + ((subNode.ax() - beforeSize) | 0)) | 0);
      mapNode.bd = ((mapNode.bd + ((subNode.dB() - beforeHash) | 0)) | 0);
      return (void 0);
    } else {
      $p_sci_HashMapBuilder__insertValue__sci_BitmapIndexedMapNode__I__O__I__I__O__V(this, mapNode, bitpos, key, originalHash, keyHash, value);
      return (void 0);
    }
  }
  if ((mapNode instanceof $c_sci_HashCollisionMapNode)) {
    var index$3 = mapNode.eT(key);
    if ((index$3 < 0)) {
      mapNode.a1 = mapNode.a1.dz(new $c_T2(key, value));
      return (void 0);
    } else {
      mapNode.a1 = mapNode.a1.dG(index$3, new $c_T2(key, value));
      return (void 0);
    }
  }
  throw new $c_s_MatchError(mapNode);
});
$p.jt = (function() {
  if ((this.cg.aE === 0)) {
    return $m_sci_HashMap$().ij;
  } else if ((this.ex !== null)) {
    return this.ex;
  } else {
    this.ex = new $c_sci_HashMap(this.cg);
    return this.ex;
  }
});
$p.n3 = (function(elem) {
  $p_sci_HashMapBuilder__ensureUnaliased__V(this);
  var h = $m_sr_Statics$().C(elem.aZ);
  var im = $m_sc_Hashing$().c0(h);
  this.eY(this.cg, elem.aZ, elem.aQ, h, im, 0);
  return this;
});
$p.dY = (function(key, value) {
  $p_sci_HashMapBuilder__ensureUnaliased__V(this);
  var originalHash = $m_sr_Statics$().C(key);
  this.eY(this.cg, key, value, originalHash, $m_sc_Hashing$().c0(originalHash), 0);
  return this;
});
$p.iG = (function(xs) {
  $p_sci_HashMapBuilder__ensureUnaliased__V(this);
  if ((xs instanceof $c_sci_HashMap)) {
    new $c_sci_HashMapBuilder$$anon$1(xs, this);
  } else if (false) {
    var iter = xs.rR();
    while (iter.m()) {
      var next = iter.g();
      var originalHash = xs.rC(next.nE());
      var hash = $m_sc_Hashing$().c0(originalHash);
      this.eY(this.cg, next.nL(), next.op(), originalHash, hash, 0);
    }
  } else if (false) {
    var iter$2 = xs.pQ();
    while (iter$2.m()) {
      var next$2 = iter$2.g();
      var originalHash$2 = xs.rC(next$2.nE());
      var hash$2 = $m_sc_Hashing$().c0(originalHash$2);
      this.eY(this.cg, next$2.nL(), next$2.op(), originalHash$2, hash$2, 0);
    }
  } else if ($is_sci_Map(xs)) {
    xs.e1(new $c_sr_AbstractFunction2_$$Lambda$b4228bd32034ae3b2f0c5fc896319aa4b79b55f8(((key$2, value$2) => this.dY(key$2, value$2))));
  } else {
    var it = xs.i();
    while (it.m()) {
      this.n3(it.g());
    }
  }
  return this;
});
$p.b2 = (function() {
  return this.jt();
});
$p.aV = (function(elem) {
  return this.n3(elem);
});
$p.aU = (function(elems) {
  return this.iG(elems);
});
var $d_sci_HashMapBuilder = new $TypeData().i($c_sci_HashMapBuilder, "scala.collection.immutable.HashMapBuilder", ({
  fO: 1,
  G: 1,
  I: 1,
  M: 1,
  a7: 1
}));
/** @constructor */
function $c_sci_LazyList$LazyBuilder() {
  this.ey = null;
  this.mg = null;
  this.pr();
}
$p = $c_sci_LazyList$LazyBuilder.prototype = new $h_O();
$p.constructor = $c_sci_LazyList$LazyBuilder;
/** @constructor */
function $h_sci_LazyList$LazyBuilder() {
}
$h_sci_LazyList$LazyBuilder.prototype = $p;
$p.aX = (function(size) {
});
$p.pr = (function() {
  var deferred = new $c_sci_LazyList$LazyBuilder$DeferredState();
  this.mg = ($m_sci_LazyList$(), $ct_sci_LazyList__O__(new $c_sci_LazyList(), new $c_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c((() => deferred.iV()))));
  this.ey = deferred;
});
$p.r6 = (function() {
  this.ey.jb(new $c_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c((() => $m_sci_LazyList$().a2)));
  return this.mg;
});
$p.p0 = (function(elem) {
  var deferred = new $c_sci_LazyList$LazyBuilder$DeferredState();
  this.ey.jb(new $c_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c((() => {
    $m_sci_LazyList$();
    return $ct_sci_LazyList__O__sci_LazyList__(new $c_sci_LazyList(), elem, ($m_sci_LazyList$(), $ct_sci_LazyList__O__(new $c_sci_LazyList(), new $c_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c((() => deferred.iV())))));
  })));
  this.ey = deferred;
  return this;
});
$p.oR = (function(xs) {
  if ((xs.x() !== 0)) {
    var deferred = new $c_sci_LazyList$LazyBuilder$DeferredState();
    this.ey.jb(new $c_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c((() => $m_sci_LazyList$().o9(xs.i(), new $c_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c((() => deferred.iV()))))));
    this.ey = deferred;
  }
  return this;
});
$p.b2 = (function() {
  return this.r6();
});
$p.aV = (function(elem) {
  return this.p0(elem);
});
$p.aU = (function(elems) {
  return this.oR(elems);
});
var $d_sci_LazyList$LazyBuilder = new $TypeData().i($c_sci_LazyList$LazyBuilder, "scala.collection.immutable.LazyList$LazyBuilder", ({
  fV: 1,
  G: 1,
  I: 1,
  M: 1,
  a7: 1
}));
/** @constructor */
function $c_sci_LazyList$LazyIterator(lazyList) {
  this.ez = null;
  this.ez = lazyList;
}
$p = $c_sci_LazyList$LazyIterator.prototype = new $h_sc_AbstractIterator();
$p.constructor = $c_sci_LazyList$LazyIterator;
/** @constructor */
function $h_sci_LazyList$LazyIterator() {
}
$h_sci_LazyList$LazyIterator.prototype = $p;
$p.m = (function() {
  return (!($p_sci_LazyList__evaluated__sci_LazyList(this.ez) === $m_sci_LazyList$().a2));
});
$p.g = (function() {
  if (($p_sci_LazyList__evaluated__sci_LazyList(this.ez) === $m_sci_LazyList$().a2)) {
    return $m_sc_Iterator$().O.g();
  } else {
    var res = this.ez.n();
    this.ez = this.ez.b3();
    return res;
  }
});
var $d_sci_LazyList$LazyIterator = new $TypeData().i($c_sci_LazyList$LazyIterator, "scala.collection.immutable.LazyList$LazyIterator", ({
  fX: 1,
  t: 1,
  b: 1,
  c: 1,
  u: 1
}));
/** @constructor */
function $c_sci_List$() {
  $n_sci_List$ = this;
  var _1 = $m_sci_Nil$();
  $m_sci_Nil$();
}
$p = $c_sci_List$.prototype = new $h_O();
$p.constructor = $c_sci_List$;
/** @constructor */
function $h_sci_List$() {
}
$h_sci_List$.prototype = $p;
$p.cT = (function(elems) {
  return $m_sci_Nil$().eU(elems);
});
$p.aW = (function() {
  return new $c_scm_ListBuffer();
});
$p.ag = (function(source) {
  return $m_sci_Nil$().eU(source);
});
var $d_sci_List$ = new $TypeData().i($c_sci_List$, "scala.collection.immutable.List$", ({
  g0: 1,
  a: 1,
  K: 1,
  a0: 1,
  ah: 1
}));
var $n_sci_List$;
function $m_sci_List$() {
  if ((!$n_sci_List$)) {
    $n_sci_List$ = new $c_sci_List$();
  }
  return $n_sci_List$;
}
function $ct_sci_Map$Map2$Map2Iterator__sci_Map$Map2__($thiz, outer) {
  if ((outer === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
  $thiz.eA = outer;
  $thiz.df = 0;
  return $thiz;
}
/** @constructor */
function $c_sci_Map$Map2$Map2Iterator() {
  this.df = 0;
  this.eA = null;
}
$p = $c_sci_Map$Map2$Map2Iterator.prototype = new $h_sc_AbstractIterator();
$p.constructor = $c_sci_Map$Map2$Map2Iterator;
/** @constructor */
function $h_sci_Map$Map2$Map2Iterator() {
}
$h_sci_Map$Map2$Map2Iterator.prototype = $p;
$p.m = (function() {
  return (this.df < 2);
});
$p.g = (function() {
  matchResult5$1: {
    var result;
    var x23 = this.df;
    if ((x23 === 0)) {
      var result = new $c_T2(this.eA.bN, this.eA.cI);
      break matchResult5$1;
    }
    if ((x23 === 1)) {
      var result = new $c_T2(this.eA.bO, this.eA.cJ);
      break matchResult5$1;
    }
    var result = $m_sc_Iterator$().O.g();
  }
  this.df = ((1 + this.df) | 0);
  return result;
});
$p.dC = (function(n) {
  this.df = ((this.df + n) | 0);
  return this;
});
function $ct_sci_Map$Map3$Map3Iterator__sci_Map$Map3__($thiz, outer) {
  if ((outer === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
  $thiz.dg = outer;
  $thiz.dh = 0;
  return $thiz;
}
/** @constructor */
function $c_sci_Map$Map3$Map3Iterator() {
  this.dh = 0;
  this.dg = null;
}
$p = $c_sci_Map$Map3$Map3Iterator.prototype = new $h_sc_AbstractIterator();
$p.constructor = $c_sci_Map$Map3$Map3Iterator;
/** @constructor */
function $h_sci_Map$Map3$Map3Iterator() {
}
$h_sci_Map$Map3$Map3Iterator.prototype = $p;
$p.m = (function() {
  return (this.dh < 3);
});
$p.g = (function() {
  var result;
  switch (this.dh) {
    case 0: {
      var result = new $c_T2(this.dg.bD, this.dg.ci);
      break;
    }
    case 1: {
      var result = new $c_T2(this.dg.bE, this.dg.cj);
      break;
    }
    case 2: {
      var result = new $c_T2(this.dg.bF, this.dg.ck);
      break;
    }
    default: {
      var result = $m_sc_Iterator$().O.g();
    }
  }
  this.dh = ((1 + this.dh) | 0);
  return result;
});
$p.dC = (function(n) {
  this.dh = ((this.dh + n) | 0);
  return this;
});
function $ct_sci_Map$Map4$Map4Iterator__sci_Map$Map4__($thiz, outer) {
  if ((outer === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
  $thiz.cl = outer;
  $thiz.di = 0;
  return $thiz;
}
/** @constructor */
function $c_sci_Map$Map4$Map4Iterator() {
  this.di = 0;
  this.cl = null;
}
$p = $c_sci_Map$Map4$Map4Iterator.prototype = new $h_sc_AbstractIterator();
$p.constructor = $c_sci_Map$Map4$Map4Iterator;
/** @constructor */
function $h_sci_Map$Map4$Map4Iterator() {
}
$h_sci_Map$Map4$Map4Iterator.prototype = $p;
$p.m = (function() {
  return (this.di < 4);
});
$p.g = (function() {
  var result;
  switch (this.di) {
    case 0: {
      var result = new $c_T2(this.cl.be, this.cl.bP);
      break;
    }
    case 1: {
      var result = new $c_T2(this.cl.bf, this.cl.bQ);
      break;
    }
    case 2: {
      var result = new $c_T2(this.cl.bg, this.cl.bR);
      break;
    }
    case 3: {
      var result = new $c_T2(this.cl.bh, this.cl.bS);
      break;
    }
    default: {
      var result = $m_sc_Iterator$().O.g();
    }
  }
  this.di = ((1 + this.di) | 0);
  return result;
});
$p.dC = (function(n) {
  this.di = ((this.di + n) | 0);
  return this;
});
/** @constructor */
function $c_sci_MapBuilderImpl() {
  this.cK = null;
  this.fA = false;
  this.dU = null;
  this.cK = $m_sci_Map$EmptyMap$();
  this.fA = false;
}
$p = $c_sci_MapBuilderImpl.prototype = new $h_O();
$p.constructor = $c_sci_MapBuilderImpl;
/** @constructor */
function $h_sci_MapBuilderImpl() {
}
$h_sci_MapBuilderImpl.prototype = $p;
$p.aX = (function(size) {
});
$p.o6 = (function() {
  return (this.fA ? this.dU.jt() : this.cK);
});
$p.oY = (function(key, value) {
  if (this.fA) {
    this.dU.dY(key, value);
  } else if ((this.cK.ax() < 4)) {
    this.cK = this.cK.cd(key, value);
  } else if (this.cK.bl(key)) {
    this.cK = this.cK.cd(key, value);
  } else {
    this.fA = true;
    if ((this.dU === null)) {
      this.dU = new $c_sci_HashMapBuilder();
    }
    this.cK.pn(this.dU);
    this.dU.dY(key, value);
  }
  return this;
});
$p.mY = (function(xs) {
  return (this.fA ? (this.dU.iG(xs), this) : $f_scm_Growable__addAll__sc_IterableOnce__scm_Growable(this, xs));
});
$p.b2 = (function() {
  return this.o6();
});
$p.aV = (function(elem) {
  return this.oY(elem.aZ, elem.aQ);
});
$p.aU = (function(elems) {
  return this.mY(elems);
});
var $d_sci_MapBuilderImpl = new $TypeData().i($c_sci_MapBuilderImpl, "scala.collection.immutable.MapBuilderImpl", ({
  gb: 1,
  G: 1,
  I: 1,
  M: 1,
  a7: 1
}));
/** @constructor */
function $c_sci_Vector$() {
  this.mk = 0;
  this.ml = null;
  $n_sci_Vector$ = this;
  try {
    $m_sc_StringOps$();
    var $x_1 = $m_jl_Integer$().nJ($m_jl_System$SystemProperties$().j7("scala.collection.immutable.Vector.defaultApplyPreferredMaxLength", "250"), 10, 214748364);
  } catch (e) {
    if (false) {
      var $x_1 = 250;
    } else {
      var $x_1;
      throw e;
    }
  }
  this.mk = $x_1;
  this.ml = new $c_sci_NewVectorIterator($m_sci_Vector0$(), 0, 0);
}
$p = $c_sci_Vector$.prototype = new $h_O();
$p.constructor = $c_sci_Vector$;
/** @constructor */
function $h_sci_Vector$() {
}
$h_sci_Vector$.prototype = $p;
$p.cT = (function(elems) {
  return this.j3(elems);
});
$p.j3 = (function(it) {
  if ((it instanceof $c_sci_Vector)) {
    return it;
  } else {
    var knownSize = it.x();
    if ((knownSize === 0)) {
      return $m_sci_Vector0$();
    } else if (((((knownSize - 1) | 0) >>> 0) <= 31)) {
      matchResult3: {
        var $x_1;
        if ((it instanceof $c_sci_ArraySeq$ofRef)) {
          var x = it.a0().aC();
          if (((x !== null) && (x === $d_O.l()))) {
            var $x_1 = it.cf;
            break matchResult3;
          }
        }
        if ($is_sci_Iterable(it)) {
          var a1 = new $ac_O(knownSize);
          it.bI(a1, 0, 2147483647);
          var $x_1 = a1;
          break matchResult3;
        }
        var a1$2 = new $ac_O(knownSize);
        it.i().bI(a1$2, 0, 2147483647);
        var $x_1 = a1$2;
      }
      return new $c_sci_Vector1($x_1);
    } else {
      return new $c_sci_VectorBuilder().mZ(it).o7();
    }
  }
});
$p.ag = (function(source) {
  return this.j3(source);
});
$p.aW = (function() {
  return new $c_sci_VectorBuilder();
});
var $d_sci_Vector$ = new $TypeData().i($c_sci_Vector$, "scala.collection.immutable.Vector$", ({
  go: 1,
  a: 1,
  K: 1,
  a0: 1,
  ah: 1
}));
var $n_sci_Vector$;
function $m_sci_Vector$() {
  if ((!$n_sci_Vector$)) {
    $n_sci_Vector$ = new $c_sci_Vector$();
  }
  return $n_sci_Vector$;
}
function $p_sci_VectorBuilder__leftAlignPrefix__V($thiz) {
  var a = null;
  var aParent = null;
  if (($thiz.G >= 6)) {
    a = $thiz.av;
    var i = (($thiz.B >>> 25) | 0);
    if ((i > 0)) {
      var src = a;
      var dest = a;
      var length = ((64 - i) | 0);
      src.u(i, dest, 0, length);
    }
    var num = $thiz.B;
    var t = (((num >> 24) >>> 7) | 0);
    var newOffset = (((33554431 & ((num + t) | 0)) - t) | 0);
    $thiz.y = (($thiz.y - (($thiz.B - newOffset) | 0)) | 0);
    $thiz.B = newOffset;
    if (((($thiz.y >>> 25) | 0) === 0)) {
      $thiz.G = 5;
    }
    aParent = a;
    a = a.a[0];
  }
  if (($thiz.G >= 5)) {
    if ((a === null)) {
      a = $thiz.P;
    }
    var i$2 = (31 & (($thiz.B >>> 20) | 0));
    if (($thiz.G === 5)) {
      if ((i$2 > 0)) {
        var src$1 = a;
        var dest$1 = a;
        var length$1 = ((32 - i$2) | 0);
        src$1.u(i$2, dest$1, 0, length$1);
      }
      $thiz.P = a;
      var num$1 = $thiz.B;
      var t$1 = (((num$1 >> 19) >>> 12) | 0);
      var newOffset$1 = (((1048575 & ((num$1 + t$1) | 0)) - t$1) | 0);
      $thiz.y = (($thiz.y - (($thiz.B - newOffset$1) | 0)) | 0);
      $thiz.B = newOffset$1;
      if (((($thiz.y >>> 20) | 0) === 0)) {
        $thiz.G = 4;
      }
    } else {
      if ((i$2 > 0)) {
        a = $m_ju_Arrays$().Z(a, i$2, 32);
      }
      aParent.a[0] = a;
    }
    aParent = a;
    a = a.a[0];
  }
  if (($thiz.G >= 4)) {
    if ((a === null)) {
      a = $thiz.H;
    }
    var i$3 = (31 & (($thiz.B >>> 15) | 0));
    if (($thiz.G === 4)) {
      if ((i$3 > 0)) {
        var src$2 = a;
        var dest$2 = a;
        var length$2 = ((32 - i$3) | 0);
        src$2.u(i$3, dest$2, 0, length$2);
      }
      $thiz.H = a;
      var num$2 = $thiz.B;
      var t$2 = (((num$2 >> 14) >>> 17) | 0);
      var newOffset$2 = (((32767 & ((num$2 + t$2) | 0)) - t$2) | 0);
      $thiz.y = (($thiz.y - (($thiz.B - newOffset$2) | 0)) | 0);
      $thiz.B = newOffset$2;
      if (((($thiz.y >>> 15) | 0) === 0)) {
        $thiz.G = 3;
      }
    } else {
      if ((i$3 > 0)) {
        a = $m_ju_Arrays$().Z(a, i$3, 32);
      }
      aParent.a[0] = a;
    }
    aParent = a;
    a = a.a[0];
  }
  if (($thiz.G >= 3)) {
    if ((a === null)) {
      a = $thiz.D;
    }
    var i$4 = (31 & (($thiz.B >>> 10) | 0));
    if (($thiz.G === 3)) {
      if ((i$4 > 0)) {
        var src$3 = a;
        var dest$3 = a;
        var length$3 = ((32 - i$4) | 0);
        src$3.u(i$4, dest$3, 0, length$3);
      }
      $thiz.D = a;
      var num$3 = $thiz.B;
      var t$3 = (((num$3 >> 9) >>> 22) | 0);
      var newOffset$3 = (((1023 & ((num$3 + t$3) | 0)) - t$3) | 0);
      $thiz.y = (($thiz.y - (($thiz.B - newOffset$3) | 0)) | 0);
      $thiz.B = newOffset$3;
      if (((($thiz.y >>> 10) | 0) === 0)) {
        $thiz.G = 2;
      }
    } else {
      if ((i$4 > 0)) {
        a = $m_ju_Arrays$().Z(a, i$4, 32);
      }
      aParent.a[0] = a;
    }
    aParent = a;
    a = a.a[0];
  }
  if (($thiz.G >= 2)) {
    if ((a === null)) {
      a = $thiz.A;
    }
    var i$5 = (31 & (($thiz.B >>> 5) | 0));
    if (($thiz.G === 2)) {
      if ((i$5 > 0)) {
        var src$4 = a;
        var dest$4 = a;
        var length$4 = ((32 - i$5) | 0);
        src$4.u(i$5, dest$4, 0, length$4);
      }
      $thiz.A = a;
      var num$4 = $thiz.B;
      var t$4 = (((num$4 >> 4) >>> 27) | 0);
      var newOffset$4 = (((31 & ((num$4 + t$4) | 0)) - t$4) | 0);
      $thiz.y = (($thiz.y - (($thiz.B - newOffset$4) | 0)) | 0);
      $thiz.B = newOffset$4;
      if (((($thiz.y >>> 5) | 0) === 0)) {
        $thiz.G = 1;
      }
    } else {
      if ((i$5 > 0)) {
        a = $m_ju_Arrays$().Z(a, i$5, 32);
      }
      aParent.a[0] = a;
    }
    aParent = a;
    a = a.a[0];
  }
  if (($thiz.G >= 1)) {
    if ((a === null)) {
      a = $thiz.M;
    }
    var i$6 = (31 & $thiz.B);
    if (($thiz.G === 1)) {
      if ((i$6 > 0)) {
        var src$5 = a;
        var dest$5 = a;
        var length$5 = ((32 - i$6) | 0);
        src$5.u(i$6, dest$5, 0, length$5);
      }
      $thiz.M = a;
      $thiz.E = (($thiz.E - $thiz.B) | 0);
      $thiz.B = 0;
    } else {
      if ((i$6 > 0)) {
        a = $m_ju_Arrays$().Z(a, i$6, 32);
      }
      aParent.a[0] = a;
    }
  }
  $thiz.gL = false;
}
function $p_sci_VectorBuilder__addArr1__AO__V($thiz, data) {
  var dl = data.a.length;
  if ((dl > 0)) {
    if (($thiz.E === 32)) {
      $p_sci_VectorBuilder__advance__V($thiz);
    }
    var a = ((32 - $thiz.E) | 0);
    var copy1 = ((a < dl) ? a : dl);
    var copy2 = ((dl - copy1) | 0);
    var dest = $thiz.M;
    var destPos = $thiz.E;
    data.u(0, dest, destPos, copy1);
    $thiz.E = (($thiz.E + copy1) | 0);
    if ((copy2 > 0)) {
      $p_sci_VectorBuilder__advance__V($thiz);
      var dest$1 = $thiz.M;
      data.u(copy1, dest$1, 0, copy2);
      $thiz.E = (($thiz.E + copy2) | 0);
    }
  }
}
function $p_sci_VectorBuilder__addArrN__AO__I__V($thiz, slice, dim) {
  if ((slice.a.length === 0)) {
    return (void 0);
  }
  if (($thiz.E === 32)) {
    $p_sci_VectorBuilder__advance__V($thiz);
  }
  var sl = slice.a.length;
  switch (dim) {
    case 2: {
      var a = (31 & ((((1024 - $thiz.y) | 0) >>> 5) | 0));
      var copy1 = ((a < sl) ? a : sl);
      var copy2 = ((sl - copy1) | 0);
      var destPos = (31 & (($thiz.y >>> 5) | 0));
      var dest = $thiz.A;
      slice.u(0, dest, destPos, copy1);
      $p_sci_VectorBuilder__advanceN__I__V($thiz, (copy1 << 5));
      if ((copy2 > 0)) {
        var dest$1 = $thiz.A;
        slice.u(copy1, dest$1, 0, copy2);
        $p_sci_VectorBuilder__advanceN__I__V($thiz, (copy2 << 5));
      }
      break;
    }
    case 3: {
      var num = $thiz.y;
      var t = (((num >> 9) >>> 22) | 0);
      if (((((1023 & ((num + t) | 0)) - t) | 0) !== 0)) {
        var f = ((e$3) => {
          $p_sci_VectorBuilder__addArrN__AO__I__V($thiz, e$3, 2);
        });
        var len = slice.a.length;
        var i = 0;
        if ((slice !== null)) {
          while ((i < len)) {
            var x0 = slice.a[i];
            f(x0);
            i = ((1 + i) | 0);
          }
        } else if ((slice instanceof $ac_I)) {
          while ((i < len)) {
            var x0$1 = slice.a[i];
            f(x0$1);
            i = ((1 + i) | 0);
          }
        } else if ((slice instanceof $ac_D)) {
          while ((i < len)) {
            var x0$2 = slice.a[i];
            f(x0$2);
            i = ((1 + i) | 0);
          }
        } else if ((slice instanceof $ac_J)) {
          while ((i < len)) {
            var $x_1 = slice.a;
            var $x_2 = (i << 1);
            var x0$3_$_lo = $x_1[$x_2];
            var x0$3_$_hi = $x_1[(($x_2 + 1) | 0)];
            f($bL(x0$3_$_lo, x0$3_$_hi));
            i = ((1 + i) | 0);
          }
        } else if ((slice instanceof $ac_F)) {
          while ((i < len)) {
            var x0$4 = slice.a[i];
            f(x0$4);
            i = ((1 + i) | 0);
          }
        } else if ((slice instanceof $ac_C)) {
          while ((i < len)) {
            var x0$5 = slice.a[i];
            f($bC(x0$5));
            i = ((1 + i) | 0);
          }
        } else if ((slice instanceof $ac_B)) {
          while ((i < len)) {
            var x0$6 = slice.a[i];
            f(x0$6);
            i = ((1 + i) | 0);
          }
        } else if ((slice instanceof $ac_S)) {
          while ((i < len)) {
            var x0$7 = slice.a[i];
            f(x0$7);
            i = ((1 + i) | 0);
          }
        } else if ((slice instanceof $ac_Z)) {
          while ((i < len)) {
            var x0$8 = slice.a[i];
            f(x0$8);
            i = ((1 + i) | 0);
          }
        } else {
          throw new $c_s_MatchError(slice);
        }
        return (void 0);
      }
      var a$1 = (31 & ((((32768 - $thiz.y) | 0) >>> 10) | 0));
      var copy1$2 = ((a$1 < sl) ? a$1 : sl);
      var copy2$2 = ((sl - copy1$2) | 0);
      var destPos$2 = (31 & (($thiz.y >>> 10) | 0));
      var dest$2 = $thiz.D;
      slice.u(0, dest$2, destPos$2, copy1$2);
      $p_sci_VectorBuilder__advanceN__I__V($thiz, (copy1$2 << 10));
      if ((copy2$2 > 0)) {
        var dest$3 = $thiz.D;
        slice.u(copy1$2, dest$3, 0, copy2$2);
        $p_sci_VectorBuilder__advanceN__I__V($thiz, (copy2$2 << 10));
      }
      break;
    }
    case 4: {
      var num$1 = $thiz.y;
      var t$1 = (((num$1 >> 14) >>> 17) | 0);
      if (((((32767 & ((num$1 + t$1) | 0)) - t$1) | 0) !== 0)) {
        var f$1 = ((e$3$1) => {
          $p_sci_VectorBuilder__addArrN__AO__I__V($thiz, e$3$1, 3);
        });
        var len$1 = slice.a.length;
        var i$1 = 0;
        if ((slice !== null)) {
          while ((i$1 < len$1)) {
            var x0$9 = slice.a[i$1];
            f$1(x0$9);
            i$1 = ((1 + i$1) | 0);
          }
        } else if ((slice instanceof $ac_I)) {
          while ((i$1 < len$1)) {
            var x0$10 = slice.a[i$1];
            f$1(x0$10);
            i$1 = ((1 + i$1) | 0);
          }
        } else if ((slice instanceof $ac_D)) {
          while ((i$1 < len$1)) {
            var x0$11 = slice.a[i$1];
            f$1(x0$11);
            i$1 = ((1 + i$1) | 0);
          }
        } else if ((slice instanceof $ac_J)) {
          while ((i$1 < len$1)) {
            var $x_3 = slice.a;
            var $x_4 = (i$1 << 1);
            var x0$12_$_lo = $x_3[$x_4];
            var x0$12_$_hi = $x_3[(($x_4 + 1) | 0)];
            f$1($bL(x0$12_$_lo, x0$12_$_hi));
            i$1 = ((1 + i$1) | 0);
          }
        } else if ((slice instanceof $ac_F)) {
          while ((i$1 < len$1)) {
            var x0$13 = slice.a[i$1];
            f$1(x0$13);
            i$1 = ((1 + i$1) | 0);
          }
        } else if ((slice instanceof $ac_C)) {
          while ((i$1 < len$1)) {
            var x0$14 = slice.a[i$1];
            f$1($bC(x0$14));
            i$1 = ((1 + i$1) | 0);
          }
        } else if ((slice instanceof $ac_B)) {
          while ((i$1 < len$1)) {
            var x0$15 = slice.a[i$1];
            f$1(x0$15);
            i$1 = ((1 + i$1) | 0);
          }
        } else if ((slice instanceof $ac_S)) {
          while ((i$1 < len$1)) {
            var x0$16 = slice.a[i$1];
            f$1(x0$16);
            i$1 = ((1 + i$1) | 0);
          }
        } else if ((slice instanceof $ac_Z)) {
          while ((i$1 < len$1)) {
            var x0$17 = slice.a[i$1];
            f$1(x0$17);
            i$1 = ((1 + i$1) | 0);
          }
        } else {
          throw new $c_s_MatchError(slice);
        }
        return (void 0);
      }
      var a$2 = (31 & ((((1048576 - $thiz.y) | 0) >>> 15) | 0));
      var copy1$3 = ((a$2 < sl) ? a$2 : sl);
      var copy2$3 = ((sl - copy1$3) | 0);
      var destPos$3 = (31 & (($thiz.y >>> 15) | 0));
      var dest$4 = $thiz.H;
      slice.u(0, dest$4, destPos$3, copy1$3);
      $p_sci_VectorBuilder__advanceN__I__V($thiz, (copy1$3 << 15));
      if ((copy2$3 > 0)) {
        var dest$5 = $thiz.H;
        slice.u(copy1$3, dest$5, 0, copy2$3);
        $p_sci_VectorBuilder__advanceN__I__V($thiz, (copy2$3 << 15));
      }
      break;
    }
    case 5: {
      var num$2 = $thiz.y;
      var t$2 = (((num$2 >> 19) >>> 12) | 0);
      if (((((1048575 & ((num$2 + t$2) | 0)) - t$2) | 0) !== 0)) {
        var f$2 = ((e$3$2) => {
          $p_sci_VectorBuilder__addArrN__AO__I__V($thiz, e$3$2, 4);
        });
        var len$2 = slice.a.length;
        var i$2 = 0;
        if ((slice !== null)) {
          while ((i$2 < len$2)) {
            var x0$18 = slice.a[i$2];
            f$2(x0$18);
            i$2 = ((1 + i$2) | 0);
          }
        } else if ((slice instanceof $ac_I)) {
          while ((i$2 < len$2)) {
            var x0$19 = slice.a[i$2];
            f$2(x0$19);
            i$2 = ((1 + i$2) | 0);
          }
        } else if ((slice instanceof $ac_D)) {
          while ((i$2 < len$2)) {
            var x0$20 = slice.a[i$2];
            f$2(x0$20);
            i$2 = ((1 + i$2) | 0);
          }
        } else if ((slice instanceof $ac_J)) {
          while ((i$2 < len$2)) {
            var $x_5 = slice.a;
            var $x_6 = (i$2 << 1);
            var x0$21_$_lo = $x_5[$x_6];
            var x0$21_$_hi = $x_5[(($x_6 + 1) | 0)];
            f$2($bL(x0$21_$_lo, x0$21_$_hi));
            i$2 = ((1 + i$2) | 0);
          }
        } else if ((slice instanceof $ac_F)) {
          while ((i$2 < len$2)) {
            var x0$22 = slice.a[i$2];
            f$2(x0$22);
            i$2 = ((1 + i$2) | 0);
          }
        } else if ((slice instanceof $ac_C)) {
          while ((i$2 < len$2)) {
            var x0$23 = slice.a[i$2];
            f$2($bC(x0$23));
            i$2 = ((1 + i$2) | 0);
          }
        } else if ((slice instanceof $ac_B)) {
          while ((i$2 < len$2)) {
            var x0$24 = slice.a[i$2];
            f$2(x0$24);
            i$2 = ((1 + i$2) | 0);
          }
        } else if ((slice instanceof $ac_S)) {
          while ((i$2 < len$2)) {
            var x0$25 = slice.a[i$2];
            f$2(x0$25);
            i$2 = ((1 + i$2) | 0);
          }
        } else if ((slice instanceof $ac_Z)) {
          while ((i$2 < len$2)) {
            var x0$26 = slice.a[i$2];
            f$2(x0$26);
            i$2 = ((1 + i$2) | 0);
          }
        } else {
          throw new $c_s_MatchError(slice);
        }
        return (void 0);
      }
      var a$3 = (31 & ((((33554432 - $thiz.y) | 0) >>> 20) | 0));
      var copy1$4 = ((a$3 < sl) ? a$3 : sl);
      var copy2$4 = ((sl - copy1$4) | 0);
      var destPos$4 = (31 & (($thiz.y >>> 20) | 0));
      var dest$6 = $thiz.P;
      slice.u(0, dest$6, destPos$4, copy1$4);
      $p_sci_VectorBuilder__advanceN__I__V($thiz, (copy1$4 << 20));
      if ((copy2$4 > 0)) {
        var dest$7 = $thiz.P;
        slice.u(copy1$4, dest$7, 0, copy2$4);
        $p_sci_VectorBuilder__advanceN__I__V($thiz, (copy2$4 << 20));
      }
      break;
    }
    case 6: {
      var num$3 = $thiz.y;
      var t$3 = (((num$3 >> 24) >>> 7) | 0);
      if (((((33554431 & ((num$3 + t$3) | 0)) - t$3) | 0) !== 0)) {
        var f$3 = ((e$3$3) => {
          $p_sci_VectorBuilder__addArrN__AO__I__V($thiz, e$3$3, 5);
        });
        var len$3 = slice.a.length;
        var i$3 = 0;
        if ((slice !== null)) {
          while ((i$3 < len$3)) {
            var x0$27 = slice.a[i$3];
            f$3(x0$27);
            i$3 = ((1 + i$3) | 0);
          }
        } else if ((slice instanceof $ac_I)) {
          while ((i$3 < len$3)) {
            var x0$28 = slice.a[i$3];
            f$3(x0$28);
            i$3 = ((1 + i$3) | 0);
          }
        } else if ((slice instanceof $ac_D)) {
          while ((i$3 < len$3)) {
            var x0$29 = slice.a[i$3];
            f$3(x0$29);
            i$3 = ((1 + i$3) | 0);
          }
        } else if ((slice instanceof $ac_J)) {
          while ((i$3 < len$3)) {
            var $x_7 = slice.a;
            var $x_8 = (i$3 << 1);
            var x0$30_$_lo = $x_7[$x_8];
            var x0$30_$_hi = $x_7[(($x_8 + 1) | 0)];
            f$3($bL(x0$30_$_lo, x0$30_$_hi));
            i$3 = ((1 + i$3) | 0);
          }
        } else if ((slice instanceof $ac_F)) {
          while ((i$3 < len$3)) {
            var x0$31 = slice.a[i$3];
            f$3(x0$31);
            i$3 = ((1 + i$3) | 0);
          }
        } else if ((slice instanceof $ac_C)) {
          while ((i$3 < len$3)) {
            var x0$32 = slice.a[i$3];
            f$3($bC(x0$32));
            i$3 = ((1 + i$3) | 0);
          }
        } else if ((slice instanceof $ac_B)) {
          while ((i$3 < len$3)) {
            var x0$33 = slice.a[i$3];
            f$3(x0$33);
            i$3 = ((1 + i$3) | 0);
          }
        } else if ((slice instanceof $ac_S)) {
          while ((i$3 < len$3)) {
            var x0$34 = slice.a[i$3];
            f$3(x0$34);
            i$3 = ((1 + i$3) | 0);
          }
        } else if ((slice instanceof $ac_Z)) {
          while ((i$3 < len$3)) {
            var x0$35 = slice.a[i$3];
            f$3(x0$35);
            i$3 = ((1 + i$3) | 0);
          }
        } else {
          throw new $c_s_MatchError(slice);
        }
        return (void 0);
      }
      var destPos$5 = (($thiz.y >>> 25) | 0);
      if ((((destPos$5 + sl) | 0) > 64)) {
        throw $ct_jl_IllegalArgumentException__T__(new $c_jl_IllegalArgumentException(), "exceeding 2^31 elements");
      }
      var dest$8 = $thiz.av;
      slice.u(0, dest$8, destPos$5, sl);
      $p_sci_VectorBuilder__advanceN__I__V($thiz, (sl << 25));
      break;
    }
    default: {
      throw new $c_s_MatchError(dim);
    }
  }
}
function $p_sci_VectorBuilder__addVector__sci_Vector__sci_VectorBuilder($thiz, xs) {
  var sliceCount = xs.cx();
  var sliceIdx = 0;
  while ((sliceIdx < sliceCount)) {
    var slice = xs.cw(sliceIdx);
    matchResult26: {
      var idx = sliceIdx;
      var c = (((sliceCount + ((sliceCount >>> 31) | 0)) | 0) >> 1);
      var a = ((idx - c) | 0);
      var sign = (a >> 31);
      var x37 = ((((1 + c) | 0) - (((a ^ sign) - sign) | 0)) | 0);
      if ((x37 === 1)) {
        $p_sci_VectorBuilder__addArr1__AO__V($thiz, slice);
        break matchResult26;
      }
      if ((($thiz.E === 32) || ($thiz.E === 0))) {
        $p_sci_VectorBuilder__addArrN__AO__I__V($thiz, slice, x37);
        break matchResult26;
      }
      $m_sci_VectorStatics$().iZ(((x37 - 2) | 0), slice, new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((data$3) => {
        $p_sci_VectorBuilder__addArr1__AO__V($thiz, data$3);
      })));
    }
    sliceIdx = ((1 + sliceIdx) | 0);
  }
  return $thiz;
}
function $p_sci_VectorBuilder__advance__V($thiz) {
  var idx = ((32 + $thiz.y) | 0);
  var xor = (idx ^ $thiz.y);
  $thiz.y = idx;
  $thiz.E = 0;
  $p_sci_VectorBuilder__advance1__I__I__V($thiz, idx, xor);
}
function $p_sci_VectorBuilder__advanceN__I__V($thiz, n) {
  if ((n > 0)) {
    var idx = (($thiz.y + n) | 0);
    var xor = (idx ^ $thiz.y);
    $thiz.y = idx;
    $thiz.E = 0;
    $p_sci_VectorBuilder__advance1__I__I__V($thiz, idx, xor);
  }
}
function $p_sci_VectorBuilder__advance1__I__I__V($thiz, idx, xor) {
  if ((xor <= 0)) {
    throw $ct_jl_IllegalArgumentException__T__(new $c_jl_IllegalArgumentException(), ((((((((((((((((("advance1(" + idx) + ", ") + xor) + "): a1=") + $thiz.M) + ", a2=") + $thiz.A) + ", a3=") + $thiz.D) + ", a4=") + $thiz.H) + ", a5=") + $thiz.P) + ", a6=") + $thiz.av) + ", depth=") + $thiz.G));
  } else if ((xor < 1024)) {
    if (($thiz.G <= 1)) {
      $thiz.A = new ($d_O.r().r().C)(32);
      $thiz.A.a[0] = $thiz.M;
      $thiz.G = 2;
    }
    $thiz.M = new $ac_O(32);
    $thiz.A.a[(31 & ((idx >>> 5) | 0))] = $thiz.M;
  } else if ((xor < 32768)) {
    if (($thiz.G <= 2)) {
      $thiz.D = new ($d_O.r().r().r().C)(32);
      $thiz.D.a[0] = $thiz.A;
      $thiz.G = 3;
    }
    $thiz.M = new $ac_O(32);
    $thiz.A = new ($d_O.r().r().C)(32);
    $thiz.A.a[(31 & ((idx >>> 5) | 0))] = $thiz.M;
    $thiz.D.a[(31 & ((idx >>> 10) | 0))] = $thiz.A;
  } else if ((xor < 1048576)) {
    if (($thiz.G <= 3)) {
      $thiz.H = new ($d_O.r().r().r().r().C)(32);
      $thiz.H.a[0] = $thiz.D;
      $thiz.G = 4;
    }
    $thiz.M = new $ac_O(32);
    $thiz.A = new ($d_O.r().r().C)(32);
    $thiz.D = new ($d_O.r().r().r().C)(32);
    $thiz.A.a[(31 & ((idx >>> 5) | 0))] = $thiz.M;
    $thiz.D.a[(31 & ((idx >>> 10) | 0))] = $thiz.A;
    $thiz.H.a[(31 & ((idx >>> 15) | 0))] = $thiz.D;
  } else if ((xor < 33554432)) {
    if (($thiz.G <= 4)) {
      $thiz.P = new ($d_O.r().r().r().r().r().C)(32);
      $thiz.P.a[0] = $thiz.H;
      $thiz.G = 5;
    }
    $thiz.M = new $ac_O(32);
    $thiz.A = new ($d_O.r().r().C)(32);
    $thiz.D = new ($d_O.r().r().r().C)(32);
    $thiz.H = new ($d_O.r().r().r().r().C)(32);
    $thiz.A.a[(31 & ((idx >>> 5) | 0))] = $thiz.M;
    $thiz.D.a[(31 & ((idx >>> 10) | 0))] = $thiz.A;
    $thiz.H.a[(31 & ((idx >>> 15) | 0))] = $thiz.D;
    $thiz.P.a[(31 & ((idx >>> 20) | 0))] = $thiz.H;
  } else {
    if (($thiz.G <= 5)) {
      $thiz.av = new ($d_O.r().r().r().r().r().r().C)(64);
      $thiz.av.a[0] = $thiz.P;
      $thiz.G = 6;
    }
    $thiz.M = new $ac_O(32);
    $thiz.A = new ($d_O.r().r().C)(32);
    $thiz.D = new ($d_O.r().r().r().C)(32);
    $thiz.H = new ($d_O.r().r().r().r().C)(32);
    $thiz.P = new ($d_O.r().r().r().r().r().C)(32);
    $thiz.A.a[(31 & ((idx >>> 5) | 0))] = $thiz.M;
    $thiz.D.a[(31 & ((idx >>> 10) | 0))] = $thiz.A;
    $thiz.H.a[(31 & ((idx >>> 15) | 0))] = $thiz.D;
    $thiz.P.a[(31 & ((idx >>> 20) | 0))] = $thiz.H;
    $thiz.av.a[((idx >>> 25) | 0)] = $thiz.P;
  }
}
/** @constructor */
function $c_sci_VectorBuilder() {
  this.av = null;
  this.P = null;
  this.H = null;
  this.D = null;
  this.A = null;
  this.M = null;
  this.E = 0;
  this.y = 0;
  this.B = 0;
  this.gL = false;
  this.G = 0;
  this.M = new $ac_O(32);
  this.E = 0;
  this.y = 0;
  this.B = 0;
  this.gL = false;
  this.G = 1;
}
$p = $c_sci_VectorBuilder.prototype = new $h_O();
$p.constructor = $c_sci_VectorBuilder;
/** @constructor */
function $h_sci_VectorBuilder() {
}
$h_sci_VectorBuilder.prototype = $p;
$p.aX = (function(size) {
});
$p.qm = (function(v) {
  var x28 = v.cx();
  switch (x28) {
    case 0: {
      break;
    }
    case 1: {
      this.G = 1;
      var i = v.d.a.length;
      this.E = (31 & i);
      this.y = ((i - this.E) | 0);
      var a = v.d;
      this.M = ((a.a.length === 32) ? a : $m_ju_Arrays$().Z(a, 0, 32));
      break;
    }
    case 3: {
      var d2 = v.bj;
      var a$1 = v.f;
      this.M = ((a$1.a.length === 32) ? a$1 : $m_ju_Arrays$().Z(a$1, 0, 32));
      this.G = 2;
      this.B = ((32 - v.bG) | 0);
      var i$1 = ((v.h + this.B) | 0);
      this.E = (31 & i$1);
      this.y = ((i$1 - this.E) | 0);
      this.A = new ($d_O.r().r().C)(32);
      this.A.a[0] = v.d;
      var dest = this.A;
      var length = d2.a.length;
      d2.u(0, dest, 1, length);
      this.A.a[((1 + d2.a.length) | 0)] = this.M;
      break;
    }
    case 5: {
      var d3 = v.aR;
      var s2 = v.aS;
      var a$2 = v.f;
      this.M = ((a$2.a.length === 32) ? a$2 : $m_ju_Arrays$().Z(a$2, 0, 32));
      this.G = 3;
      this.B = ((1024 - v.ba) | 0);
      var i$2 = ((v.h + this.B) | 0);
      this.E = (31 & i$2);
      this.y = ((i$2 - this.E) | 0);
      this.D = new ($d_O.r().r().r().C)(32);
      this.D.a[0] = $m_sci_VectorStatics$().cp(v.d, v.bw);
      var dest$1 = this.D;
      var length$1 = d3.a.length;
      d3.u(0, dest$1, 1, length$1);
      this.A = $m_ju_Arrays$().S(s2, 32);
      this.D.a[((1 + d3.a.length) | 0)] = this.A;
      this.A.a[s2.a.length] = this.M;
      break;
    }
    case 7: {
      var d4 = v.as;
      var s3 = v.au;
      var s2$2 = v.at;
      var a$3 = v.f;
      this.M = ((a$3.a.length === 32) ? a$3 : $m_ju_Arrays$().Z(a$3, 0, 32));
      this.G = 4;
      this.B = ((32768 - v.aJ) | 0);
      var i$3 = ((v.h + this.B) | 0);
      this.E = (31 & i$3);
      this.y = ((i$3 - this.E) | 0);
      this.H = new ($d_O.r().r().r().r().C)(32);
      this.H.a[0] = $m_sci_VectorStatics$().cp($m_sci_VectorStatics$().cp(v.d, v.b0), v.b1);
      var dest$2 = this.H;
      var length$2 = d4.a.length;
      d4.u(0, dest$2, 1, length$2);
      this.D = $m_ju_Arrays$().S(s3, 32);
      this.A = $m_ju_Arrays$().S(s2$2, 32);
      this.H.a[((1 + d4.a.length) | 0)] = this.D;
      this.D.a[s3.a.length] = this.A;
      this.A.a[s2$2.a.length] = this.M;
      break;
    }
    case 9: {
      var d5 = v.a3;
      var s4 = v.a6;
      var s3$2 = v.a5;
      var s2$3 = v.a4;
      var a$4 = v.f;
      this.M = ((a$4.a.length === 32) ? a$4 : $m_ju_Arrays$().Z(a$4, 0, 32));
      this.G = 5;
      this.B = ((1048576 - v.am) | 0);
      var i$4 = ((v.h + this.B) | 0);
      this.E = (31 & i$4);
      this.y = ((i$4 - this.E) | 0);
      this.P = new ($d_O.r().r().r().r().r().C)(32);
      this.P.a[0] = $m_sci_VectorStatics$().cp($m_sci_VectorStatics$().cp($m_sci_VectorStatics$().cp(v.d, v.ay), v.az), v.aA);
      var dest$3 = this.P;
      var length$3 = d5.a.length;
      d5.u(0, dest$3, 1, length$3);
      this.H = $m_ju_Arrays$().S(s4, 32);
      this.D = $m_ju_Arrays$().S(s3$2, 32);
      this.A = $m_ju_Arrays$().S(s2$3, 32);
      this.P.a[((1 + d5.a.length) | 0)] = this.H;
      this.H.a[s4.a.length] = this.D;
      this.D.a[s3$2.a.length] = this.A;
      this.A.a[s2$3.a.length] = this.M;
      break;
    }
    case 11: {
      var d6 = v.U;
      var s5 = v.Y;
      var s4$2 = v.X;
      var s3$3 = v.W;
      var s2$4 = v.V;
      var a$5 = v.f;
      this.M = ((a$5.a.length === 32) ? a$5 : $m_ju_Arrays$().Z(a$5, 0, 32));
      this.G = 6;
      this.B = ((33554432 - v.af) | 0);
      var i$5 = ((v.h + this.B) | 0);
      this.E = (31 & i$5);
      this.y = ((i$5 - this.E) | 0);
      this.av = new ($d_O.r().r().r().r().r().r().C)(64);
      this.av.a[0] = $m_sci_VectorStatics$().cp($m_sci_VectorStatics$().cp($m_sci_VectorStatics$().cp($m_sci_VectorStatics$().cp(v.d, v.an), v.ao), v.ap), v.aq);
      var dest$4 = this.av;
      var length$4 = d6.a.length;
      d6.u(0, dest$4, 1, length$4);
      this.P = $m_ju_Arrays$().S(s5, 32);
      this.H = $m_ju_Arrays$().S(s4$2, 32);
      this.D = $m_ju_Arrays$().S(s3$3, 32);
      this.A = $m_ju_Arrays$().S(s2$4, 32);
      this.av.a[((1 + d6.a.length) | 0)] = this.P;
      this.P.a[s5.a.length] = this.H;
      this.H.a[s4$2.a.length] = this.D;
      this.D.a[s3$3.a.length] = this.A;
      this.A.a[s2$4.a.length] = this.M;
      break;
    }
    default: {
      throw new $c_s_MatchError(x28);
    }
  }
  if (((this.E === 0) && (this.y > 0))) {
    this.E = 32;
    this.y = ((this.y - 32) | 0);
  }
  return this;
});
$p.p1 = (function(elem) {
  if ((this.E === 32)) {
    $p_sci_VectorBuilder__advance__V(this);
  }
  this.M.a[this.E] = elem;
  this.E = ((1 + this.E) | 0);
  return this;
});
$p.mZ = (function(xs) {
  return ((xs instanceof $c_sci_Vector) ? ((((this.E === 0) && (this.y === 0)) && (!this.gL)) ? this.qm(xs) : $p_sci_VectorBuilder__addVector__sci_Vector__sci_VectorBuilder(this, xs)) : $f_scm_Growable__addAll__sc_IterableOnce__scm_Growable(this, xs));
});
$p.o7 = (function() {
  if (this.gL) {
    $p_sci_VectorBuilder__leftAlignPrefix__V(this);
  }
  var len = ((this.E + this.y) | 0);
  var realLen = ((len - this.B) | 0);
  if ((realLen === 0)) {
    $m_sci_Vector$();
    return $m_sci_Vector0$();
  } else if ((len < 0)) {
    throw $ct_jl_IndexOutOfBoundsException__T__(new $c_jl_IndexOutOfBoundsException(), ("Vector cannot have negative size " + len));
  } else if ((len <= 32)) {
    var a = this.M;
    return new $c_sci_Vector1(((a.a.length === realLen) ? a : $m_ju_Arrays$().S(a, realLen)));
  } else if ((len <= 1024)) {
    var i1 = (31 & ((len - 1) | 0));
    var i2 = ((((len - 1) | 0) >>> 5) | 0);
    var data = $m_ju_Arrays$().Z(this.A, 1, i2);
    var prefix1 = this.A.a[0];
    var a$1 = this.A.a[i2];
    var len$1 = ((1 + i1) | 0);
    var suffix1 = ((a$1.a.length === len$1) ? a$1 : $m_ju_Arrays$().S(a$1, len$1));
    return new $c_sci_Vector2(prefix1, ((32 - this.B) | 0), data, suffix1, realLen);
  } else if ((len <= 32768)) {
    var i1$2 = (31 & ((len - 1) | 0));
    var i2$2 = (31 & ((((len - 1) | 0) >>> 5) | 0));
    var i3 = ((((len - 1) | 0) >>> 10) | 0);
    var data$2 = $m_ju_Arrays$().Z(this.D, 1, i3);
    var a$2 = this.D.a[0];
    var prefix2 = $m_ju_Arrays$().Z(a$2, 1, a$2.a.length);
    var prefix1$2 = this.D.a[0].a[0];
    var suffix2 = $m_ju_Arrays$().S(this.D.a[i3], i2$2);
    var a$3 = this.D.a[i3].a[i2$2];
    var len$2 = ((1 + i1$2) | 0);
    var suffix1$2 = ((a$3.a.length === len$2) ? a$3 : $m_ju_Arrays$().S(a$3, len$2));
    var len1 = prefix1$2.a.length;
    return new $c_sci_Vector3(prefix1$2, len1, prefix2, ((len1 + (prefix2.a.length << 5)) | 0), data$2, suffix2, suffix1$2, realLen);
  } else if ((len <= 1048576)) {
    var i1$3 = (31 & ((len - 1) | 0));
    var i2$3 = (31 & ((((len - 1) | 0) >>> 5) | 0));
    var i3$2 = (31 & ((((len - 1) | 0) >>> 10) | 0));
    var i4 = ((((len - 1) | 0) >>> 15) | 0);
    var data$3 = $m_ju_Arrays$().Z(this.H, 1, i4);
    var a$4 = this.H.a[0];
    var prefix3 = $m_ju_Arrays$().Z(a$4, 1, a$4.a.length);
    var a$5 = this.H.a[0].a[0];
    var prefix2$2 = $m_ju_Arrays$().Z(a$5, 1, a$5.a.length);
    var prefix1$3 = this.H.a[0].a[0].a[0];
    var suffix3 = $m_ju_Arrays$().S(this.H.a[i4], i3$2);
    var suffix2$2 = $m_ju_Arrays$().S(this.H.a[i4].a[i3$2], i2$3);
    var a$6 = this.H.a[i4].a[i3$2].a[i2$3];
    var len$3 = ((1 + i1$3) | 0);
    var suffix1$3 = ((a$6.a.length === len$3) ? a$6 : $m_ju_Arrays$().S(a$6, len$3));
    var len1$2 = prefix1$3.a.length;
    var len12$2 = ((len1$2 + (prefix2$2.a.length << 5)) | 0);
    return new $c_sci_Vector4(prefix1$3, len1$2, prefix2$2, len12$2, prefix3, ((len12$2 + (prefix3.a.length << 10)) | 0), data$3, suffix3, suffix2$2, suffix1$3, realLen);
  } else if ((len <= 33554432)) {
    var i1$4 = (31 & ((len - 1) | 0));
    var i2$4 = (31 & ((((len - 1) | 0) >>> 5) | 0));
    var i3$3 = (31 & ((((len - 1) | 0) >>> 10) | 0));
    var i4$2 = (31 & ((((len - 1) | 0) >>> 15) | 0));
    var i5 = ((((len - 1) | 0) >>> 20) | 0);
    var data$4 = $m_ju_Arrays$().Z(this.P, 1, i5);
    var a$7 = this.P.a[0];
    var prefix4 = $m_ju_Arrays$().Z(a$7, 1, a$7.a.length);
    var a$8 = this.P.a[0].a[0];
    var prefix3$2 = $m_ju_Arrays$().Z(a$8, 1, a$8.a.length);
    var a$9 = this.P.a[0].a[0].a[0];
    var prefix2$3 = $m_ju_Arrays$().Z(a$9, 1, a$9.a.length);
    var prefix1$4 = this.P.a[0].a[0].a[0].a[0];
    var suffix4 = $m_ju_Arrays$().S(this.P.a[i5], i4$2);
    var suffix3$2 = $m_ju_Arrays$().S(this.P.a[i5].a[i4$2], i3$3);
    var suffix2$3 = $m_ju_Arrays$().S(this.P.a[i5].a[i4$2].a[i3$3], i2$4);
    var a$10 = this.P.a[i5].a[i4$2].a[i3$3].a[i2$4];
    var len$4 = ((1 + i1$4) | 0);
    var suffix1$4 = ((a$10.a.length === len$4) ? a$10 : $m_ju_Arrays$().S(a$10, len$4));
    var len1$3 = prefix1$4.a.length;
    var len12$3 = ((len1$3 + (prefix2$3.a.length << 5)) | 0);
    var len123$2 = ((len12$3 + (prefix3$2.a.length << 10)) | 0);
    return new $c_sci_Vector5(prefix1$4, len1$3, prefix2$3, len12$3, prefix3$2, len123$2, prefix4, ((len123$2 + (prefix4.a.length << 15)) | 0), data$4, suffix4, suffix3$2, suffix2$3, suffix1$4, realLen);
  } else {
    var i1$5 = (31 & ((len - 1) | 0));
    var i2$5 = (31 & ((((len - 1) | 0) >>> 5) | 0));
    var i3$4 = (31 & ((((len - 1) | 0) >>> 10) | 0));
    var i4$3 = (31 & ((((len - 1) | 0) >>> 15) | 0));
    var i5$2 = (31 & ((((len - 1) | 0) >>> 20) | 0));
    var i6 = ((((len - 1) | 0) >>> 25) | 0);
    var data$5 = $m_ju_Arrays$().Z(this.av, 1, i6);
    var a$11 = this.av.a[0];
    var prefix5 = $m_ju_Arrays$().Z(a$11, 1, a$11.a.length);
    var a$12 = this.av.a[0].a[0];
    var prefix4$2 = $m_ju_Arrays$().Z(a$12, 1, a$12.a.length);
    var a$13 = this.av.a[0].a[0].a[0];
    var prefix3$3 = $m_ju_Arrays$().Z(a$13, 1, a$13.a.length);
    var a$14 = this.av.a[0].a[0].a[0].a[0];
    var prefix2$4 = $m_ju_Arrays$().Z(a$14, 1, a$14.a.length);
    var prefix1$5 = this.av.a[0].a[0].a[0].a[0].a[0];
    var suffix5 = $m_ju_Arrays$().S(this.av.a[i6], i5$2);
    var suffix4$2 = $m_ju_Arrays$().S(this.av.a[i6].a[i5$2], i4$3);
    var suffix3$3 = $m_ju_Arrays$().S(this.av.a[i6].a[i5$2].a[i4$3], i3$4);
    var suffix2$4 = $m_ju_Arrays$().S(this.av.a[i6].a[i5$2].a[i4$3].a[i3$4], i2$5);
    var a$15 = this.av.a[i6].a[i5$2].a[i4$3].a[i3$4].a[i2$5];
    var len$5 = ((1 + i1$5) | 0);
    var suffix1$5 = ((a$15.a.length === len$5) ? a$15 : $m_ju_Arrays$().S(a$15, len$5));
    var len1$4 = prefix1$5.a.length;
    var len12$4 = ((len1$4 + (prefix2$4.a.length << 5)) | 0);
    var len123$3 = ((len12$4 + (prefix3$3.a.length << 10)) | 0);
    var len1234$2 = ((len123$3 + (prefix4$2.a.length << 15)) | 0);
    return new $c_sci_Vector6(prefix1$5, len1$4, prefix2$4, len12$4, prefix3$3, len123$3, prefix4$2, len1234$2, prefix5, ((len1234$2 + (prefix5.a.length << 20)) | 0), data$5, suffix5, suffix4$2, suffix3$3, suffix2$4, suffix1$5, realLen);
  }
});
$p.t = (function() {
  return (((((((("VectorBuilder(len1=" + this.E) + ", lenRest=") + this.y) + ", offset=") + this.B) + ", depth=") + this.G) + ")");
});
$p.aV = (function(elem) {
  return this.p1(elem);
});
$p.aU = (function(elems) {
  return this.mZ(elems);
});
$p.b2 = (function() {
  return this.o7();
});
var $d_sci_VectorBuilder = new $TypeData().i($c_sci_VectorBuilder, "scala.collection.immutable.VectorBuilder", ({
  gw: 1,
  G: 1,
  I: 1,
  M: 1,
  a7: 1
}));
/** @constructor */
function $c_scm_ArrayBuffer$() {
  this.mn = null;
  $n_scm_ArrayBuffer$ = this;
  this.mn = new $ac_O(0);
}
$p = $c_scm_ArrayBuffer$.prototype = new $h_O();
$p.constructor = $c_scm_ArrayBuffer$;
/** @constructor */
function $h_scm_ArrayBuffer$() {
}
$h_scm_ArrayBuffer$.prototype = $p;
$p.cT = (function(elems) {
  return this.ny(elems);
});
$p.ny = (function(coll) {
  var k = coll.x();
  if ((k >= 0)) {
    var array = this.oa(this.mn, 0, k);
    var actual = ($is_sc_Iterable(coll) ? coll.bI(array, 0, 2147483647) : coll.i().bI(array, 0, 2147483647));
    if ((actual !== k)) {
      throw new $c_jl_IllegalStateException(((("Copied " + actual) + " of ") + k));
    }
    return $ct_scm_ArrayBuffer__AO__I__(new $c_scm_ArrayBuffer(), array, k);
  } else {
    return $ct_scm_ArrayBuffer__(new $c_scm_ArrayBuffer()).n0(coll);
  }
});
$p.aW = (function() {
  return new $c_scm_ArrayBuffer$$anon$1();
});
$p.r5 = (function(arrayLen, targetLen) {
  if ((targetLen < 0)) {
    throw $ct_jl_RuntimeException__T__(new $c_jl_RuntimeException(), ((((("Overflow while resizing array of array-backed collection. Requested length: " + targetLen) + "; current length: ") + arrayLen) + "; increase: ") + ((targetLen - arrayLen) | 0)));
  } else if ((targetLen <= arrayLen)) {
    return (-1);
  } else {
    if ((targetLen > 2147483639)) {
      throw $ct_jl_RuntimeException__T__(new $c_jl_RuntimeException(), ((("Array of array-backed collection exceeds VM length limit of 2147483639. Requested length: " + targetLen) + "; current length: ") + arrayLen));
    }
    if ((arrayLen > 1073741819)) {
      return 2147483639;
    } else {
      var x = (arrayLen << 1);
      var y = ((x > 16) ? x : 16);
      return ((targetLen > y) ? targetLen : y);
    }
  }
});
$p.oa = (function(array, curSize, targetSize) {
  var newLen = this.r5(array.a.length, targetSize);
  if ((newLen < 0)) {
    return array;
  } else {
    var res = new $ac_O(newLen);
    array.u(0, res, 0, curSize);
    return res;
  }
});
$p.ag = (function(source) {
  return this.ny(source);
});
var $d_scm_ArrayBuffer$ = new $TypeData().i($c_scm_ArrayBuffer$, "scala.collection.mutable.ArrayBuffer$", ({
  gB: 1,
  a: 1,
  K: 1,
  a0: 1,
  ah: 1
}));
var $n_scm_ArrayBuffer$;
function $m_scm_ArrayBuffer$() {
  if ((!$n_scm_ArrayBuffer$)) {
    $n_scm_ArrayBuffer$ = new $c_scm_ArrayBuffer$();
  }
  return $n_scm_ArrayBuffer$;
}
/** @constructor */
function $c_scm_ArrayBuffer$$anon$1() {
  this.ds = null;
  $ct_scm_GrowableBuilder__scm_Growable__(this, ($m_scm_ArrayBuffer$(), $ct_scm_ArrayBuffer__(new $c_scm_ArrayBuffer())));
}
$p = $c_scm_ArrayBuffer$$anon$1.prototype = new $h_scm_GrowableBuilder();
$p.constructor = $c_scm_ArrayBuffer$$anon$1;
/** @constructor */
function $h_scm_ArrayBuffer$$anon$1() {
}
$h_scm_ArrayBuffer$$anon$1.prototype = $p;
$p.aX = (function(size) {
  this.ds.aX(size);
});
var $d_scm_ArrayBuffer$$anon$1 = new $TypeData().i($c_scm_ArrayBuffer$$anon$1, "scala.collection.mutable.ArrayBuffer$$anon$1", ({
  gC: 1,
  aU: 1,
  G: 1,
  I: 1,
  M: 1
}));
/** @constructor */
function $c_scm_Buffer$() {
  this.ew = null;
  $ct_sc_SeqFactory$Delegate__sc_SeqFactory__(this, $m_sjs_js_WrappedArray$());
}
$p = $c_scm_Buffer$.prototype = new $h_sc_SeqFactory$Delegate();
$p.constructor = $c_scm_Buffer$;
/** @constructor */
function $h_scm_Buffer$() {
}
$h_scm_Buffer$.prototype = $p;
var $d_scm_Buffer$ = new $TypeData().i($c_scm_Buffer$, "scala.collection.mutable.Buffer$", ({
  gI: 1,
  bN: 1,
  a: 1,
  K: 1,
  a0: 1
}));
var $n_scm_Buffer$;
function $m_scm_Buffer$() {
  if ((!$n_scm_Buffer$)) {
    $n_scm_Buffer$ = new $c_scm_Buffer$();
  }
  return $n_scm_Buffer$;
}
/** @constructor */
function $c_scm_HashSet$$anon$4(initialCapacity$1, loadFactor$1) {
  this.ds = null;
  $ct_scm_GrowableBuilder__scm_Growable__(this, $ct_scm_HashSet__I__D__(new $c_scm_HashSet(), initialCapacity$1, loadFactor$1));
}
$p = $c_scm_HashSet$$anon$4.prototype = new $h_scm_GrowableBuilder();
$p.constructor = $c_scm_HashSet$$anon$4;
/** @constructor */
function $h_scm_HashSet$$anon$4() {
}
$h_scm_HashSet$$anon$4.prototype = $p;
$p.aX = (function(size) {
  this.ds.aX(size);
});
var $d_scm_HashSet$$anon$4 = new $TypeData().i($c_scm_HashSet$$anon$4, "scala.collection.mutable.HashSet$$anon$4", ({
  gQ: 1,
  aU: 1,
  G: 1,
  I: 1,
  M: 1
}));
function $ct_scm_HashSet$HashSetIterator__scm_HashSet__($thiz, outer) {
  if ((outer === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
  $thiz.fE = outer;
  $thiz.du = 0;
  $thiz.cP = null;
  $thiz.fF = outer.aK.a.length;
  return $thiz;
}
/** @constructor */
function $c_scm_HashSet$HashSetIterator() {
  this.du = 0;
  this.cP = null;
  this.fF = 0;
  this.fE = null;
}
$p = $c_scm_HashSet$HashSetIterator.prototype = new $h_sc_AbstractIterator();
$p.constructor = $c_scm_HashSet$HashSetIterator;
/** @constructor */
function $h_scm_HashSet$HashSetIterator() {
}
$h_scm_HashSet$HashSetIterator.prototype = $p;
$p.m = (function() {
  if ((this.cP !== null)) {
    return true;
  } else {
    while ((this.du < this.fF)) {
      var n = this.fE.aK.a[this.du];
      this.du = ((1 + this.du) | 0);
      if ((n !== null)) {
        this.cP = n;
        return true;
      }
    }
    return false;
  }
});
$p.g = (function() {
  if ((!this.m())) {
    return $m_sc_Iterator$().O.g();
  } else {
    var x$proxy10 = this.cP;
    if ((x$proxy10 === null)) {
      $m_sr_Scala3RunTime$().bp();
    }
    var r = this.iX(x$proxy10);
    var x$proxy11 = this.cP;
    if ((x$proxy11 === null)) {
      $m_sr_Scala3RunTime$().bp();
    }
    this.cP = x$proxy11.aL;
    return r;
  }
});
function $ct_scm_ImmutableBuilder__sc_IterableOnce__($thiz, empty) {
  $thiz.fG = empty;
  return $thiz;
}
/** @constructor */
function $c_scm_ImmutableBuilder() {
  this.fG = null;
}
$p = $c_scm_ImmutableBuilder.prototype = new $h_O();
$p.constructor = $c_scm_ImmutableBuilder;
/** @constructor */
function $h_scm_ImmutableBuilder() {
}
$h_scm_ImmutableBuilder.prototype = $p;
$p.aU = (function(elems) {
  return $f_scm_Growable__addAll__sc_IterableOnce__scm_Growable(this, elems);
});
$p.aX = (function(size) {
});
$p.b2 = (function() {
  return this.fG;
});
/** @constructor */
function $c_scm_IndexedSeq$() {
  this.ew = null;
  $ct_sc_SeqFactory$Delegate__sc_SeqFactory__(this, $m_scm_ArrayBuffer$());
}
$p = $c_scm_IndexedSeq$.prototype = new $h_sc_SeqFactory$Delegate();
$p.constructor = $c_scm_IndexedSeq$;
/** @constructor */
function $h_scm_IndexedSeq$() {
}
$h_scm_IndexedSeq$.prototype = $p;
var $d_scm_IndexedSeq$ = new $TypeData().i($c_scm_IndexedSeq$, "scala.collection.mutable.IndexedSeq$", ({
  gT: 1,
  bN: 1,
  a: 1,
  K: 1,
  a0: 1
}));
var $n_scm_IndexedSeq$;
function $m_scm_IndexedSeq$() {
  if ((!$n_scm_IndexedSeq$)) {
    $n_scm_IndexedSeq$ = new $c_scm_IndexedSeq$();
  }
  return $n_scm_IndexedSeq$;
}
/** @constructor */
function $c_scm_ListBuffer$() {
}
$p = $c_scm_ListBuffer$.prototype = new $h_O();
$p.constructor = $c_scm_ListBuffer$;
/** @constructor */
function $h_scm_ListBuffer$() {
}
$h_scm_ListBuffer$.prototype = $p;
$p.cT = (function(elems) {
  return new $c_scm_ListBuffer().hl(elems);
});
$p.aW = (function() {
  return $ct_scm_GrowableBuilder__scm_Growable__(new $c_scm_GrowableBuilder(), new $c_scm_ListBuffer());
});
$p.ag = (function(source) {
  return new $c_scm_ListBuffer().hl(source);
});
var $d_scm_ListBuffer$ = new $TypeData().i($c_scm_ListBuffer$, "scala.collection.mutable.ListBuffer$", ({
  gW: 1,
  a: 1,
  K: 1,
  a0: 1,
  ah: 1
}));
var $n_scm_ListBuffer$;
function $m_scm_ListBuffer$() {
  if ((!$n_scm_ListBuffer$)) {
    $n_scm_ListBuffer$ = new $c_scm_ListBuffer$();
  }
  return $n_scm_ListBuffer$;
}
/** @constructor */
function $c_scm_MutationTracker$CheckedIterator(underlying, mutationCount) {
  this.iy = null;
  this.mx = null;
  this.mw = 0;
  this.iy = underlying;
  this.mx = mutationCount;
  this.mw = (mutationCount.F() | 0);
}
$p = $c_scm_MutationTracker$CheckedIterator.prototype = new $h_sc_AbstractIterator();
$p.constructor = $c_scm_MutationTracker$CheckedIterator;
/** @constructor */
function $h_scm_MutationTracker$CheckedIterator() {
}
$h_scm_MutationTracker$CheckedIterator.prototype = $p;
$p.m = (function() {
  $m_scm_MutationTracker$().nd(this.mw, (this.mx.F() | 0), "mutation occurred during iteration");
  return this.iy.m();
});
$p.g = (function() {
  return this.iy.g();
});
var $d_scm_MutationTracker$CheckedIterator = new $TypeData().i($c_scm_MutationTracker$CheckedIterator, "scala.collection.mutable.MutationTracker$CheckedIterator", ({
  gY: 1,
  t: 1,
  b: 1,
  c: 1,
  u: 1
}));
/** @constructor */
function $c_s_concurrent_ExecutionContext$parasitic$() {
  this.mB = null;
  $n_s_concurrent_ExecutionContext$parasitic$ = this;
  this.mB = new $c_jl_ThreadLocal();
}
$p = $c_s_concurrent_ExecutionContext$parasitic$.prototype = new $h_O();
$p.constructor = $c_s_concurrent_ExecutionContext$parasitic$;
/** @constructor */
function $h_s_concurrent_ExecutionContext$parasitic$() {
}
$h_s_concurrent_ExecutionContext$parasitic$.prototype = $p;
$p.iW = (function(runnable) {
  $f_s_concurrent_BatchingExecutor__submitSyncBatched__jl_Runnable__V(this, runnable);
});
$p.js = (function(t) {
  $m_s_concurrent_ExecutionContext$().eG.b(t);
});
var $d_s_concurrent_ExecutionContext$parasitic$ = new $TypeData().i($c_s_concurrent_ExecutionContext$parasitic$, "scala.concurrent.ExecutionContext$parasitic$", ({
  h6: 1,
  aW: 1,
  aF: 1,
  aX: 1,
  h2: 1
}));
var $n_s_concurrent_ExecutionContext$parasitic$;
function $m_s_concurrent_ExecutionContext$parasitic$() {
  if ((!$n_s_concurrent_ExecutionContext$parasitic$)) {
    $n_s_concurrent_ExecutionContext$parasitic$ = new $c_s_concurrent_ExecutionContext$parasitic$();
  }
  return $n_s_concurrent_ExecutionContext$parasitic$;
}
function $f_s_reflect_ClassTag__equals__O__Z($thiz, x) {
  if ($is_s_reflect_ClassTag(x)) {
    var x$2 = $thiz.aC();
    var x$3 = x.aC();
    return ((x$2 === null) ? (x$3 === null) : (x$2 === x$3));
  } else {
    return false;
  }
}
function $p_s_reflect_ClassTag__prettyprint$1__jl_Class__T($thiz, clazz) {
  return (clazz.ah.Z ? (("Array[" + $p_s_reflect_ClassTag__prettyprint$1__jl_Class__T($thiz, clazz.ah.Q())) + "]") : clazz.ah.N);
}
function $is_s_reflect_ClassTag(obj) {
  return (!(!((obj && obj.$classData) && obj.$classData.n.F)));
}
function $isArrayOf_s_reflect_ClassTag(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.F)));
}
/** @constructor */
function $c_sr_ScalaRunTime$$anon$1(x$1) {
  this.mK = null;
  this.fO = 0;
  this.mJ = 0;
  this.mK = x$1;
  this.fO = 0;
  this.mJ = x$1.aN();
}
$p = $c_sr_ScalaRunTime$$anon$1.prototype = new $h_sc_AbstractIterator();
$p.constructor = $c_sr_ScalaRunTime$$anon$1;
/** @constructor */
function $h_sr_ScalaRunTime$$anon$1() {
}
$h_sr_ScalaRunTime$$anon$1.prototype = $p;
$p.m = (function() {
  return (this.fO < this.mJ);
});
$p.g = (function() {
  var result = this.mK.aO(this.fO);
  this.fO = ((1 + this.fO) | 0);
  return result;
});
var $d_sr_ScalaRunTime$$anon$1 = new $TypeData().i($c_sr_ScalaRunTime$$anon$1, "scala.runtime.ScalaRunTime$$anon$1", ({
  hT: 1,
  t: 1,
  b: 1,
  c: 1,
  u: 1
}));
/** @constructor */
function $c_sjs_js_WrappedArray$() {
}
$p = $c_sjs_js_WrappedArray$.prototype = new $h_O();
$p.constructor = $c_sjs_js_WrappedArray$;
/** @constructor */
function $h_sjs_js_WrappedArray$() {
}
$h_sjs_js_WrappedArray$.prototype = $p;
$p.cT = (function(elems) {
  return this.nz(elems);
});
$p.aW = (function() {
  return $ct_sjs_js_WrappedArray__(new $c_sjs_js_WrappedArray());
});
$p.nz = (function(source) {
  return $f_scm_Growable__addAll__sc_IterableOnce__scm_Growable($ct_sjs_js_WrappedArray__(new $c_sjs_js_WrappedArray()), source).b2();
});
$p.ag = (function(source) {
  return this.nz(source);
});
var $d_sjs_js_WrappedArray$ = new $TypeData().i($c_sjs_js_WrappedArray$, "scala.scalajs.js.WrappedArray$", ({
  i5: 1,
  ah: 1,
  a: 1,
  K: 1,
  a0: 1
}));
var $n_sjs_js_WrappedArray$;
function $m_sjs_js_WrappedArray$() {
  if ((!$n_sjs_js_WrappedArray$)) {
    $n_sjs_js_WrappedArray$ = new $c_sjs_js_WrappedArray$();
  }
  return $n_sjs_js_WrappedArray$;
}
/** @constructor */
function $c_sjsr_WrappedVarArgs$() {
}
$p = $c_sjsr_WrappedVarArgs$.prototype = new $h_O();
$p.constructor = $c_sjsr_WrappedVarArgs$;
/** @constructor */
function $h_sjsr_WrappedVarArgs$() {
}
$h_sjsr_WrappedVarArgs$.prototype = $p;
$p.cT = (function(elems) {
  return this.j4(elems);
});
$p.j4 = (function(source) {
  return this.aW().aU(source).b2();
});
$p.aW = (function() {
  return new $c_scm_Builder$$anon$1(new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((x$1$2$2) => new $c_sjsr_WrappedVarArgs(x$1$2$2.dw))), $ct_sjs_js_WrappedArray__sjs_js_Array__(new $c_sjs_js_WrappedArray(), []));
});
$p.ag = (function(source) {
  return this.j4(source);
});
var $d_sjsr_WrappedVarArgs$ = new $TypeData().i($c_sjsr_WrappedVarArgs$, "scala.scalajs.runtime.WrappedVarArgs$", ({
  ik: 1,
  ah: 1,
  a: 1,
  K: 1,
  a0: 1
}));
var $n_sjsr_WrappedVarArgs$;
function $m_sjsr_WrappedVarArgs$() {
  if ((!$n_sjsr_WrappedVarArgs$)) {
    $n_sjsr_WrappedVarArgs$ = new $c_sjsr_WrappedVarArgs$();
  }
  return $n_sjsr_WrappedVarArgs$;
}
/** @constructor */
function $c_s_util_Failure(exception) {
  this.c7 = null;
  this.c7 = exception;
}
$p = $c_s_util_Failure.prototype = new $h_s_util_Try();
$p.constructor = $c_s_util_Failure;
/** @constructor */
function $h_s_util_Failure() {
}
$h_s_util_Failure.prototype = $p;
$p.r = (function() {
  return $m_s_util_hashing_MurmurHash3$().e7(this, (-1408943127), true);
});
$p.k = (function(x$0) {
  if ((this === x$0)) {
    return true;
  } else if ((x$0 instanceof $c_s_util_Failure)) {
    var x = this.c7;
    var x$2 = x$0.c7;
    return ((x === null) ? (x$2 === null) : x.k(x$2));
  } else {
    return false;
  }
});
$p.t = (function() {
  return $m_sr_ScalaRunTime$().eK(this);
});
$p.aN = (function() {
  return 1;
});
$p.aP = (function() {
  return "Failure";
});
$p.aO = (function(n) {
  if ((n === 0)) {
    return this.c7;
  }
  throw $ct_jl_IndexOutOfBoundsException__I__(new $c_jl_IndexOutOfBoundsException(), n);
});
$p.nH = (function() {
  return true;
});
$p.nI = (function() {
  return false;
});
$p.s = (function() {
  var $x_1 = this.c7;
  throw (($x_1 instanceof $c_sjs_js_JavaScriptException) ? $x_1.K : $x_1);
});
$p.bm = (function(f) {
});
$p.jg = (function(f) {
  return this;
});
$p.jp = (function(pf) {
  var marker = $m_sr_Statics$PFMarker$();
  try {
    var v = pf.bX(this.c7, new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((x$2) => marker)));
    return ((marker !== v) ? new $c_s_util_Success(v) : this);
  } catch (e) {
    var e$2 = ((e instanceof $c_jl_Throwable) ? e : new $c_sjs_js_JavaScriptException(e));
    var x18 = $m_s_util_control_NonFatal$().dF(e$2);
    if ((!x18.c())) {
      return new $c_s_util_Failure(x18.s());
    }
    throw ((e$2 instanceof $c_sjs_js_JavaScriptException) ? e$2.K : e$2);
  }
});
$p.c8 = (function(fa, fb) {
  return fa.b(this.c7);
});
function $isArrayOf_s_util_Failure(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.cC)));
}
var $d_s_util_Failure = new $TypeData().i($c_s_util_Failure, "scala.util.Failure", ({
  cC: 1,
  b0: 1,
  d: 1,
  E: 1,
  a: 1
}));
/** @constructor */
function $c_s_util_Success(value) {
  this.cn = null;
  this.cn = value;
}
$p = $c_s_util_Success.prototype = new $h_s_util_Try();
$p.constructor = $c_s_util_Success;
/** @constructor */
function $h_s_util_Success() {
}
$h_s_util_Success.prototype = $p;
$p.r = (function() {
  return $m_s_util_hashing_MurmurHash3$().e7(this, (-1750213842), true);
});
$p.k = (function(x$0) {
  return ((this === x$0) || ((x$0 instanceof $c_s_util_Success) && $m_sr_BoxesRunTime$().j(this.cn, x$0.cn)));
});
$p.t = (function() {
  return $m_sr_ScalaRunTime$().eK(this);
});
$p.aN = (function() {
  return 1;
});
$p.aP = (function() {
  return "Success";
});
$p.aO = (function(n) {
  if ((n === 0)) {
    return this.cn;
  }
  throw $ct_jl_IndexOutOfBoundsException__I__(new $c_jl_IndexOutOfBoundsException(), n);
});
$p.nH = (function() {
  return false;
});
$p.nI = (function() {
  return true;
});
$p.s = (function() {
  return this.cn;
});
$p.bm = (function(f) {
  f.b(this.cn);
});
$p.jg = (function(f) {
  try {
    return new $c_s_util_Success(f.b(this.cn));
  } catch (e) {
    var e$2 = ((e instanceof $c_jl_Throwable) ? e : new $c_sjs_js_JavaScriptException(e));
    var x2 = $m_s_util_control_NonFatal$().dF(e$2);
    if ((!x2.c())) {
      return new $c_s_util_Failure(x2.s());
    }
    throw ((e$2 instanceof $c_sjs_js_JavaScriptException) ? e$2.K : e$2);
  }
});
$p.jp = (function(pf) {
  return this;
});
$p.c8 = (function(fa, fb) {
  try {
    return fb.b(this.cn);
  } catch (e) {
    var e$2 = ((e instanceof $c_jl_Throwable) ? e : new $c_sjs_js_JavaScriptException(e));
    var x42 = $m_s_util_control_NonFatal$().dF(e$2);
    if ((!x42.c())) {
      var x43 = x42.s();
      return fa.b(x43);
    }
    throw ((e$2 instanceof $c_sjs_js_JavaScriptException) ? e$2.K : e$2);
  }
});
function $isArrayOf_s_util_Success(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.cD)));
}
var $d_s_util_Success = new $TypeData().i($c_s_util_Success, "scala.util.Success", ({
  cD: 1,
  b0: 1,
  d: 1,
  E: 1,
  a: 1
}));
class $c_Lcom_raquo_airstream_core_AirstreamError$ErrorHandlingError extends $c_Lcom_raquo_airstream_core_AirstreamError {
  constructor(error, cause) {
    super();
    this.f2 = null;
    this.f1 = null;
    this.f2 = error;
    this.f1 = cause;
    $ct_jl_Throwable__T__jl_Throwable__Z__Z__(this, ((("ErrorHandlingError: " + $m_Lcom_raquo_airstream_core_AirstreamError$().e2(error)) + "; cause: ") + $m_Lcom_raquo_airstream_core_AirstreamError$().e2(cause)), null, true, true);
    this.jc(cause);
  }
  bx() {
    return new $c_s_Product$$anon$1(this);
  }
  r() {
    return $m_s_util_hashing_MurmurHash3$().h0(this, (-889275714), null);
  }
  k(x$0) {
    if ((this === x$0)) {
      return true;
    } else if ((x$0 instanceof $c_Lcom_raquo_airstream_core_AirstreamError$ErrorHandlingError)) {
      var x = this.f2;
      var x$2 = x$0.f2;
      if (((x === null) ? (x$2 === null) : x.k(x$2))) {
        var x$3 = this.f1;
        var x$4 = x$0.f1;
        return ((x$3 === null) ? (x$4 === null) : x$3.k(x$4));
      } else {
        return false;
      }
    } else {
      return false;
    }
  }
  aN() {
    return 2;
  }
  aP() {
    return "ErrorHandlingError";
  }
  aO(n) {
    if ((n === 0)) {
      return this.f2;
    }
    if ((n === 1)) {
      return this.f1;
    }
    throw $ct_jl_IndexOutOfBoundsException__T__(new $c_jl_IndexOutOfBoundsException(), ("" + n));
  }
  t() {
    return ((("ErrorHandlingError: " + this.f2) + "; cause: ") + this.f1);
  }
}
function $isArrayOf_Lcom_raquo_airstream_core_AirstreamError$ErrorHandlingError(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.b1)));
}
var $d_Lcom_raquo_airstream_core_AirstreamError$ErrorHandlingError = new $TypeData().i($c_Lcom_raquo_airstream_core_AirstreamError$ErrorHandlingError, "com.raquo.airstream.core.AirstreamError$ErrorHandlingError", ({
  b1: 1,
  ai: 1,
  s: 1,
  a: 1,
  d: 1,
  E: 1
}));
class $c_Lcom_raquo_airstream_core_AirstreamError$ObserverError extends $c_Lcom_raquo_airstream_core_AirstreamError {
  constructor(error) {
    super();
    this.f3 = null;
    this.f3 = error;
    $ct_jl_Throwable__T__jl_Throwable__Z__Z__(this, ("ObserverError: " + $m_Lcom_raquo_airstream_core_AirstreamError$().e2(error)), null, true, true);
  }
  bx() {
    return new $c_s_Product$$anon$1(this);
  }
  r() {
    return $m_s_util_hashing_MurmurHash3$().h0(this, (-889275714), null);
  }
  k(x$0) {
    if ((this === x$0)) {
      return true;
    } else if ((x$0 instanceof $c_Lcom_raquo_airstream_core_AirstreamError$ObserverError)) {
      var x = this.f3;
      var x$2 = x$0.f3;
      return ((x === null) ? (x$2 === null) : x.k(x$2));
    } else {
      return false;
    }
  }
  aN() {
    return 1;
  }
  aP() {
    return "ObserverError";
  }
  aO(n) {
    if ((n === 0)) {
      return this.f3;
    }
    throw $ct_jl_IndexOutOfBoundsException__T__(new $c_jl_IndexOutOfBoundsException(), ("" + n));
  }
  t() {
    return ("ObserverError: " + this.f3);
  }
}
function $isArrayOf_Lcom_raquo_airstream_core_AirstreamError$ObserverError(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.b2)));
}
var $d_Lcom_raquo_airstream_core_AirstreamError$ObserverError = new $TypeData().i($c_Lcom_raquo_airstream_core_AirstreamError$ObserverError, "com.raquo.airstream.core.AirstreamError$ObserverError", ({
  b2: 1,
  ai: 1,
  s: 1,
  a: 1,
  d: 1,
  E: 1
}));
class $c_Lcom_raquo_airstream_core_AirstreamError$ObserverErrorHandlingError extends $c_Lcom_raquo_airstream_core_AirstreamError {
  constructor(error, cause) {
    super();
    this.f5 = null;
    this.f4 = null;
    this.f5 = error;
    this.f4 = cause;
    $ct_jl_Throwable__T__jl_Throwable__Z__Z__(this, ((("ObserverErrorHandlingError: " + $m_Lcom_raquo_airstream_core_AirstreamError$().e2(error)) + "; cause: ") + $m_Lcom_raquo_airstream_core_AirstreamError$().e2(cause)), null, true, true);
    this.jc(cause);
  }
  bx() {
    return new $c_s_Product$$anon$1(this);
  }
  r() {
    return $m_s_util_hashing_MurmurHash3$().h0(this, (-889275714), null);
  }
  k(x$0) {
    if ((this === x$0)) {
      return true;
    } else if ((x$0 instanceof $c_Lcom_raquo_airstream_core_AirstreamError$ObserverErrorHandlingError)) {
      var x = this.f5;
      var x$2 = x$0.f5;
      if (((x === null) ? (x$2 === null) : x.k(x$2))) {
        var x$3 = this.f4;
        var x$4 = x$0.f4;
        return ((x$3 === null) ? (x$4 === null) : x$3.k(x$4));
      } else {
        return false;
      }
    } else {
      return false;
    }
  }
  aN() {
    return 2;
  }
  aP() {
    return "ObserverErrorHandlingError";
  }
  aO(n) {
    if ((n === 0)) {
      return this.f5;
    }
    if ((n === 1)) {
      return this.f4;
    }
    throw $ct_jl_IndexOutOfBoundsException__T__(new $c_jl_IndexOutOfBoundsException(), ("" + n));
  }
  t() {
    return ((("ObserverErrorHandlingError: " + this.f5) + "; cause: ") + this.f4);
  }
}
function $isArrayOf_Lcom_raquo_airstream_core_AirstreamError$ObserverErrorHandlingError(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.b3)));
}
var $d_Lcom_raquo_airstream_core_AirstreamError$ObserverErrorHandlingError = new $TypeData().i($c_Lcom_raquo_airstream_core_AirstreamError$ObserverErrorHandlingError, "com.raquo.airstream.core.AirstreamError$ObserverErrorHandlingError", ({
  b3: 1,
  ai: 1,
  s: 1,
  a: 1,
  d: 1,
  E: 1
}));
class $c_Lcom_raquo_airstream_core_AirstreamError$TransactionDepthExceeded extends $c_Lcom_raquo_airstream_core_AirstreamError {
  constructor(trx, depth) {
    super();
    this.ee = null;
    this.ed = 0;
    this.ee = trx;
    this.ed = depth;
    $ct_jl_Throwable__T__jl_Throwable__Z__Z__(this, (((("Transaction depth exceeded maxDepth = " + depth) + ": Execution of ") + trx) + " aborted. See `Transaction.maxDepth`."), null, true, true);
  }
  bx() {
    return new $c_s_Product$$anon$1(this);
  }
  r() {
    var acc = (-889275714);
    acc = $m_sr_Statics$().w(acc, $f_T__hashCode__I("TransactionDepthExceeded"));
    acc = $m_sr_Statics$().w(acc, $m_sr_Statics$().C(this.ee));
    acc = $m_sr_Statics$().w(acc, this.ed);
    return $m_sr_Statics$().ar(acc, 2);
  }
  k(x$0) {
    if ((this === x$0)) {
      return true;
    } else if ((x$0 instanceof $c_Lcom_raquo_airstream_core_AirstreamError$TransactionDepthExceeded)) {
      if ((this.ed === x$0.ed)) {
        var x = this.ee;
        var x$2 = x$0.ee;
        return ((x === null) ? (x$2 === null) : (x === x$2));
      } else {
        return false;
      }
    } else {
      return false;
    }
  }
  aN() {
    return 2;
  }
  aP() {
    return "TransactionDepthExceeded";
  }
  aO(n) {
    if ((n === 0)) {
      return this.ee;
    }
    if ((n === 1)) {
      return this.ed;
    }
    throw $ct_jl_IndexOutOfBoundsException__T__(new $c_jl_IndexOutOfBoundsException(), ("" + n));
  }
  t() {
    return ((("TransactionDepthExceeded: " + this.ee) + "; maxDepth: ") + this.ed);
  }
}
function $isArrayOf_Lcom_raquo_airstream_core_AirstreamError$TransactionDepthExceeded(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.b4)));
}
var $d_Lcom_raquo_airstream_core_AirstreamError$TransactionDepthExceeded = new $TypeData().i($c_Lcom_raquo_airstream_core_AirstreamError$TransactionDepthExceeded, "com.raquo.airstream.core.AirstreamError$TransactionDepthExceeded", ({
  b4: 1,
  ai: 1,
  s: 1,
  a: 1,
  d: 1,
  E: 1
}));
class $c_Lcom_raquo_airstream_core_AirstreamError$VarError extends $c_Lcom_raquo_airstream_core_AirstreamError {
  constructor(message, cause) {
    super();
    this.f7 = null;
    this.f6 = null;
    this.f7 = message;
    this.f6 = cause;
    $ct_jl_Throwable__T__jl_Throwable__Z__Z__(this, $m_Lcom_raquo_airstream_core_AirstreamError$().pu(message, cause), null, true, true);
    if ((!cause.c())) {
      this.jc(cause.s());
    }
  }
  bx() {
    return new $c_s_Product$$anon$1(this);
  }
  r() {
    return $m_s_util_hashing_MurmurHash3$().h0(this, (-889275714), null);
  }
  k(x$0) {
    if ((this === x$0)) {
      return true;
    } else if ((x$0 instanceof $c_Lcom_raquo_airstream_core_AirstreamError$VarError)) {
      if ((this.f7 === x$0.f7)) {
        var x = this.f6;
        var x$2 = x$0.f6;
        return ((x === null) ? (x$2 === null) : x.k(x$2));
      } else {
        return false;
      }
    } else {
      return false;
    }
  }
  aN() {
    return 2;
  }
  aP() {
    return "VarError";
  }
  aO(n) {
    if ((n === 0)) {
      return this.f7;
    }
    if ((n === 1)) {
      return this.f6;
    }
    throw $ct_jl_IndexOutOfBoundsException__T__(new $c_jl_IndexOutOfBoundsException(), ("" + n));
  }
  t() {
    return ((("VarError: " + this.f7) + "; cause: ") + this.f6);
  }
}
function $isArrayOf_Lcom_raquo_airstream_core_AirstreamError$VarError(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.b5)));
}
var $d_Lcom_raquo_airstream_core_AirstreamError$VarError = new $TypeData().i($c_Lcom_raquo_airstream_core_AirstreamError$VarError, "com.raquo.airstream.core.AirstreamError$VarError", ({
  b5: 1,
  ai: 1,
  s: 1,
  a: 1,
  d: 1,
  E: 1
}));
function $f_Lcom_raquo_airstream_core_Signal__onStart__V($thiz) {
  $thiz.ju();
}
function $f_Lcom_raquo_airstream_custom_CustomSource__$init$__V($thiz) {
  $thiz.jO = 1;
  $thiz.gp = 0;
}
function $f_Lcom_raquo_airstream_custom_CustomSource__onWillStart__V($thiz) {
  $thiz.gp = ((1 + $thiz.gp) | 0);
  $thiz.go.jI.F();
}
function $f_Lcom_raquo_airstream_custom_CustomSource__onStart__V($thiz) {
  try {
    var $x_1 = new $c_s_util_Success(($thiz.go.jG.F(), (void 0)));
  } catch (e) {
    var e$2 = ((e instanceof $c_jl_Throwable) ? e : new $c_sjs_js_JavaScriptException(e));
    matchResult1: {
      var $x_1;
      var x2 = $m_s_util_control_NonFatal$().dF(e$2);
      if ((!x2.c())) {
        var $x_1 = new $c_s_util_Failure(x2.s());
        break matchResult1;
      }
      throw ((e$2 instanceof $c_sjs_js_JavaScriptException) ? e$2.K : e$2);
    }
  }
  $x_1.jp(new $c_Lcom_raquo_airstream_custom_CustomSource$$anon$1($thiz));
}
function $f_Lcom_raquo_airstream_custom_CustomSource__onStop__V($thiz) {
  $thiz.go.jH.F();
}
/** @constructor */
function $c_Lcom_raquo_airstream_state_SourceVar(initial) {
  this.kd = null;
  this.ke = null;
  this.hC = null;
  this.hB = null;
  this.c3 = null;
  this.kd = (void 0);
  $f_Lcom_raquo_airstream_state_Var__$init$__V(this);
  this.hC = initial;
  this.hB = new $c_Lcom_raquo_airstream_state_VarSignal(this.hC, new $c_sjsr_AnonFunction0_$$Lambda$2bf0f8dc580d6edeb2d6a336c52a1bab3049702d((() => $f_Lcom_raquo_airstream_core_Named__displayName__T(this))));
  this.c3 = this.hB;
}
$p = $c_Lcom_raquo_airstream_state_SourceVar.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_airstream_state_SourceVar;
/** @constructor */
function $h_Lcom_raquo_airstream_state_SourceVar() {
}
$h_Lcom_raquo_airstream_state_SourceVar.prototype = $p;
$p.e3 = (function() {
  return this.kd;
});
$p.e0 = (function() {
  return $f_Lcom_raquo_airstream_core_Named__defaultDisplayName__T(this);
});
$p.t = (function() {
  return $f_Lcom_raquo_airstream_core_Named__displayName__T(this);
});
$p.oc = (function(value, transaction) {
  this.hC = value;
  $f_Lcom_raquo_airstream_core_WritableSignal__fireTry__s_util_Try__Lcom_raquo_airstream_core_Transaction__V(this.hB, value, transaction);
});
$p.gi = (function() {
  return this.c3;
});
var $d_Lcom_raquo_airstream_state_SourceVar = new $TypeData().i($c_Lcom_raquo_airstream_state_SourceVar, "com.raquo.airstream.state.SourceVar", ({
  d5: 1,
  aj: 1,
  aB: 1,
  aq: 1,
  a5: 1,
  d7: 1
}));
function $p_Lcom_raquo_laminar_nodes_ReactiveHtmlElement__appendControllablePropBinder__T__V($thiz, propDomName) {
  var x = $thiz.hY;
  if ((x === (void 0))) {
    $thiz.hY = $m_sjs_js_defined$().na($m_Lcom_raquo_ew_JsArray$().bb($m_sr_ScalaRunTime$().b4(new ($d_T.r().C)([propDomName]))));
  } else {
    (x.push(propDomName) | 0);
  }
}
function $p_Lcom_raquo_laminar_nodes_ReactiveHtmlElement__hasController__T__Z($thiz, propDomName) {
  var x = $thiz.lI;
  if ((x !== (void 0))) {
    _return: {
      var len = (x.length | 0);
      var i = 0;
      while ((i < len)) {
        if ((x[i].rT() === propDomName)) {
          var $x_1 = i;
          break _return;
        }
        i = ((1 + i) | 0);
      }
      var $x_1 = (-1);
    }
    return ($x_1 >= 0);
  } else {
    return false;
  }
}
/** @constructor */
function $c_Lcom_raquo_laminar_nodes_ReactiveHtmlElement(tag, ref) {
  this.fb = null;
  this.c4 = null;
  this.hX = null;
  this.dM = null;
  this.fc = null;
  this.hZ = null;
  this.b5 = null;
  this.lI = null;
  this.hY = null;
  this.hZ = tag;
  this.b5 = ref;
  this.fb = $m_s_None$();
  $f_Lcom_raquo_laminar_nodes_ParentNode__$init$__V(this);
  $f_Lcom_raquo_laminar_nodes_ReactiveElement__$init$__V(this);
  this.lI = (void 0);
  this.hY = (void 0);
}
$p = $c_Lcom_raquo_laminar_nodes_ReactiveHtmlElement.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_nodes_ReactiveHtmlElement;
/** @constructor */
function $h_Lcom_raquo_laminar_nodes_ReactiveHtmlElement() {
}
$h_Lcom_raquo_laminar_nodes_ReactiveHtmlElement.prototype = $p;
$p.iM = (function() {
  return this.fb;
});
$p.co = (function(parentNode) {
  $m_Lcom_raquo_laminar_nodes_ParentNode$().eL(parentNode, this, (void 0));
});
$p.h3 = (function() {
  return this.c4;
});
$p.ng = (function(x$0) {
  this.c4 = x$0;
});
$p.ec = (function(maybeNextParent) {
  $f_Lcom_raquo_laminar_nodes_ReactiveElement__willSetParent__s_Option__V(this, maybeNextParent);
});
$p.e9 = (function(maybeNextParent) {
  $f_Lcom_raquo_laminar_nodes_ReactiveElement__setParent__s_Option__V(this, maybeNextParent);
});
$p.pw = (function() {
  if ($m_Lcom_raquo_laminar_DomApi$().nG(this.b5)) {
    var x1 = this.hZ;
    if (false) {
      return x1.rM();
    }
    return (void 0);
  } else {
    return $m_Lcom_raquo_laminar_inputs_InputController$().lr;
  }
});
$p.qs = (function(propDomName) {
  var x = this.pw();
  return ((x !== (void 0)) && $m_Lcom_raquo_ew_JsArray$RichJsArray$().qj(x, propDomName, 0));
});
$p.qJ = (function(key) {
  if ((key instanceof $c_Lcom_raquo_laminar_keys_HtmlProp)) {
    if (this.qs(key.cB)) {
      if ($p_Lcom_raquo_laminar_nodes_ReactiveHtmlElement__hasController__T__Z(this, key.cB)) {
        throw $ct_jl_Exception__T__(new $c_jl_Exception(), (((((("Can not add uncontrolled `" + key.cB) + " <-- ???` to element `") + $m_Lcom_raquo_laminar_DomApi$().nj(this.b5)) + "` that already has an input controller for `") + key.cB) + "` property."));
      } else {
        $p_Lcom_raquo_laminar_nodes_ReactiveHtmlElement__appendControllablePropBinder__T__V(this, key.cB);
      }
    }
  }
});
$p.t = (function() {
  return (("ReactiveHtmlElement(" + ((this.b5 !== null) ? this.b5.outerHTML : ("tag=" + this.hZ.i2))) + ")");
});
$p.I = (function() {
  return this.b5;
});
var $d_Lcom_raquo_laminar_nodes_ReactiveHtmlElement = new $TypeData().i($c_Lcom_raquo_laminar_nodes_ReactiveHtmlElement, "com.raquo.laminar.nodes.ReactiveHtmlElement", ({
  eh: 1,
  as: 1,
  X: 1,
  aC: 1,
  bk: 1,
  ef: 1
}));
function $ct_jl_ArrayIndexOutOfBoundsException__T__($thiz, s) {
  $ct_jl_Throwable__T__jl_Throwable__Z__Z__($thiz, s, null, true, true);
  return $thiz;
}
function $ct_jl_ArrayIndexOutOfBoundsException__($thiz) {
  $ct_jl_Throwable__T__jl_Throwable__Z__Z__($thiz, null, null, true, true);
  return $thiz;
}
class $c_jl_ArrayIndexOutOfBoundsException extends $c_jl_IndexOutOfBoundsException {
}
var $d_jl_ArrayIndexOutOfBoundsException = new $TypeData().i($c_jl_ArrayIndexOutOfBoundsException, "java.lang.ArrayIndexOutOfBoundsException", ({
  ew: 1,
  by: 1,
  D: 1,
  B: 1,
  s: 1,
  a: 1
}));
function $f_jl_Double__equals__O__Z($thiz, that) {
  return Object.is($thiz, that);
}
function $f_jl_Double__hashCode__I($thiz) {
  var valueInt = ($thiz | 0);
  if (((valueInt === $thiz) && ((1.0 / $thiz) !== (-Infinity)))) {
    return valueInt;
  } else if (($thiz !== $thiz)) {
    return 2146959360;
  } else {
    var fpBitsDataView = $fpBitsDataView;
    fpBitsDataView.setFloat64(0, $thiz, true);
    return ((fpBitsDataView.getInt32(0, true) | 0) ^ (fpBitsDataView.getInt32(4, true) | 0));
  }
}
function $f_jl_Double__toString__T($thiz) {
  return ("" + $thiz);
}
function $isArrayOf_jl_Double(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.bv)));
}
var $d_jl_Double = new $TypeData().i(0, "java.lang.Double", ({
  bv: 1,
  a8: 1,
  a: 1,
  a1: 1,
  Y: 1,
  al: 1
}), ((x) => ((typeof x) === "number")));
function $f_jl_Float__equals__O__Z($thiz, that) {
  return Object.is($thiz, that);
}
function $f_jl_Float__hashCode__I($thiz) {
  var value = $thiz;
  var valueInt = (value | 0);
  if (((valueInt === value) && ((1.0 / value) !== (-Infinity)))) {
    return valueInt;
  } else if ((value !== value)) {
    return 2146959360;
  } else {
    var fpBitsDataView = $fpBitsDataView;
    fpBitsDataView.setFloat64(0, value, true);
    return ((fpBitsDataView.getInt32(0, true) | 0) ^ (fpBitsDataView.getInt32(4, true) | 0));
  }
}
function $f_jl_Float__toString__T($thiz) {
  return ("" + $thiz);
}
var $d_jl_Float = new $TypeData().i(0, "java.lang.Float", ({
  eC: 1,
  a8: 1,
  a: 1,
  a1: 1,
  Y: 1,
  al: 1
}), ((x) => $isFloat(x)));
function $f_jl_Integer__equals__O__Z($thiz, that) {
  return Object.is($thiz, that);
}
function $f_jl_Integer__hashCode__I($thiz) {
  return $thiz;
}
function $f_jl_Integer__toString__T($thiz) {
  return ("" + $thiz);
}
var $d_jl_Integer = new $TypeData().i(0, "java.lang.Integer", ({
  eE: 1,
  a8: 1,
  a: 1,
  a1: 1,
  Y: 1,
  al: 1
}), ((x) => $isInt(x)));
function $f_jl_Long__equals__O__Z($thiz, $thizhi, that) {
  if ((that instanceof $Long)) {
    var $x_1 = that;
    var this$1_$_lo = $x_1.l;
    var this$1_$_hi = $x_1.h;
    return ((($thiz ^ this$1_$_lo) | ($thizhi ^ this$1_$_hi)) === 0);
  } else {
    return false;
  }
}
function $f_jl_Long__hashCode__I($thiz, $thizhi) {
  return ($thiz ^ $thizhi);
}
function $f_jl_Long__toString__T($thiz, $thizhi) {
  return $m_RTLong$().oi($thiz, $thizhi);
}
function $isArrayOf_jl_Long(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.bz)));
}
var $d_jl_Long = new $TypeData().i(0, "java.lang.Long", ({
  bz: 1,
  a8: 1,
  a: 1,
  a1: 1,
  Y: 1,
  al: 1
}), ((x) => (x instanceof $Long)));
class $c_jl_NumberFormatException extends $c_jl_IllegalArgumentException {
  constructor(s) {
    super();
    $ct_jl_Throwable__T__jl_Throwable__Z__Z__(this, s, null, true, true);
  }
}
var $d_jl_NumberFormatException = new $TypeData().i($c_jl_NumberFormatException, "java.lang.NumberFormatException", ({
  eL: 1,
  bx: 1,
  D: 1,
  B: 1,
  s: 1,
  a: 1
}));
function $f_T__hashCode__I($thiz) {
  var n = $thiz.length;
  var h = 0;
  var i = 0;
  while ((i !== n)) {
    h = (((((h << 5) - h) | 0) + $thiz.charCodeAt(i)) | 0);
    i = ((1 + i) | 0);
  }
  return h;
}
function $f_T__equals__O__Z($thiz, that) {
  return ($thiz === that);
}
function $f_T__indexOf__I__I($thiz, ch) {
  var str = $m_jl_Character$().rA(ch);
  return ($thiz.indexOf(str) | 0);
}
function $f_T__trim__T($thiz) {
  var len = $thiz.length;
  var start = 0;
  while (((start !== len) && ($thiz.charCodeAt(start) <= 32))) {
    start = ((1 + start) | 0);
  }
  if ((start === len)) {
    return "";
  } else {
    var end = len;
    while (($thiz.charCodeAt(((end - 1) | 0)) <= 32)) {
      end = ((end - 1) | 0);
    }
    if (((start | (end ^ len)) === 0)) {
      return $thiz;
    } else {
      var beginIndex = start;
      var endIndex = end;
      return $thiz.substring(beginIndex, endIndex);
    }
  }
}
function $f_T__toString__T($thiz) {
  return $thiz;
}
function $isArrayOf_T(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.bB)));
}
var $d_T = new $TypeData().i(0, "java.lang.String", ({
  bB: 1,
  a: 1,
  a1: 1,
  aD: 1,
  Y: 1,
  al: 1
}), ((x) => ((typeof x) === "string")));
/** @constructor */
function $c_s_None$() {
}
$p = $c_s_None$.prototype = new $h_s_Option();
$p.constructor = $c_s_None$;
/** @constructor */
function $h_s_None$() {
}
$h_s_None$.prototype = $p;
$p.r = (function() {
  return 2433880;
});
$p.t = (function() {
  return "None";
});
$p.aN = (function() {
  return 0;
});
$p.aP = (function() {
  return "None";
});
$p.aO = (function(n) {
  throw $ct_jl_IndexOutOfBoundsException__I__(new $c_jl_IndexOutOfBoundsException(), n);
});
$p.q8 = (function() {
  throw $ct_ju_NoSuchElementException__T__(new $c_ju_NoSuchElementException(), "None.get");
});
$p.s = (function() {
  this.q8();
});
var $d_s_None$ = new $TypeData().i($c_s_None$, "scala.None$", ({
  fb: 1,
  bE: 1,
  b: 1,
  d: 1,
  E: 1,
  a: 1
}));
var $n_s_None$;
function $m_s_None$() {
  if ((!$n_s_None$)) {
    $n_s_None$ = new $c_s_None$();
  }
  return $n_s_None$;
}
/** @constructor */
function $c_s_Some(value) {
  this.cC = null;
  this.cC = value;
}
$p = $c_s_Some.prototype = new $h_s_Option();
$p.constructor = $c_s_Some;
/** @constructor */
function $h_s_Some() {
}
$h_s_Some.prototype = $p;
$p.r = (function() {
  return $m_s_util_hashing_MurmurHash3$().e7(this, 1323286827, true);
});
$p.k = (function(x$0) {
  return ((this === x$0) || ((x$0 instanceof $c_s_Some) && $m_sr_BoxesRunTime$().j(this.cC, x$0.cC)));
});
$p.t = (function() {
  return $m_sr_ScalaRunTime$().eK(this);
});
$p.aN = (function() {
  return 1;
});
$p.aP = (function() {
  return "Some";
});
$p.aO = (function(n) {
  if ((n === 0)) {
    return this.cC;
  }
  throw $ct_jl_IndexOutOfBoundsException__I__(new $c_jl_IndexOutOfBoundsException(), n);
});
$p.s = (function() {
  return this.cC;
});
function $isArrayOf_s_Some(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.bF)));
}
var $d_s_Some = new $TypeData().i($c_s_Some, "scala.Some", ({
  bF: 1,
  bE: 1,
  b: 1,
  d: 1,
  E: 1,
  a: 1
}));
/** @constructor */
function $c_sc_AbstractIterable() {
}
$p = $c_sc_AbstractIterable.prototype = new $h_O();
$p.constructor = $c_sc_AbstractIterable;
/** @constructor */
function $h_sc_AbstractIterable() {
}
$h_sc_AbstractIterable.prototype = $p;
$p.x = (function() {
  return (-1);
});
$p.bm = (function(f) {
  $f_sc_IterableOnceOps__foreach__F1__V(this, f);
});
$p.eQ = (function(p) {
  return $f_sc_IterableOnceOps__forall__F1__Z(this, p);
});
$p.c = (function() {
  return $f_sc_IterableOnceOps__isEmpty__Z(this);
});
$p.ax = (function() {
  return $f_sc_IterableOnceOps__size__I(this);
});
$p.bI = (function(dest, start, n) {
  return $f_sc_IterableOnceOps__copyToArray__O__I__I__I(this, dest, start, n);
});
$p.dy = (function(b, start, sep, end) {
  return $f_sc_IterableOnceOps__addString__scm_StringBuilder__T__T__T__scm_StringBuilder(this, b, start, sep, end);
});
$p.eR = (function(coll) {
  return this.bn().ag(coll);
});
$p.g8 = (function() {
  return this.bn().aW();
});
$p.bZ = (function() {
  return this.bq();
});
$p.g2 = (function(coll) {
  return this.eR(coll);
});
/** @constructor */
function $c_sc_ArrayOps$ArrayIterator(xs) {
  this.gD = null;
  this.cD = 0;
  this.fq = 0;
  this.gD = xs;
  this.cD = 0;
  this.fq = $m_jl_reflect_Array$().bJ(this.gD);
}
$p = $c_sc_ArrayOps$ArrayIterator.prototype = new $h_sc_AbstractIterator();
$p.constructor = $c_sc_ArrayOps$ArrayIterator;
/** @constructor */
function $h_sc_ArrayOps$ArrayIterator() {
}
$h_sc_ArrayOps$ArrayIterator.prototype = $p;
$p.x = (function() {
  return ((this.fq - this.cD) | 0);
});
$p.m = (function() {
  return (this.cD < this.fq);
});
$p.g = (function() {
  if ((this.cD >= $m_jl_reflect_Array$().bJ(this.gD))) {
    $m_sc_Iterator$().O.g();
  }
  var r = $m_sr_ScalaRunTime$().dZ(this.gD, this.cD);
  this.cD = ((1 + this.cD) | 0);
  return r;
});
$p.dC = (function(n) {
  if ((n > 0)) {
    var newPos = ((this.cD + n) | 0);
    if ((newPos < 0)) {
      var $x_1 = this.fq;
    } else {
      var a = this.fq;
      var $x_1 = ((a < newPos) ? a : newPos);
    }
    this.cD = $x_1;
  }
  return this;
});
var $d_sc_ArrayOps$ArrayIterator = new $TypeData().i($c_sc_ArrayOps$ArrayIterator, "scala.collection.ArrayOps$ArrayIterator", ({
  fl: 1,
  t: 1,
  b: 1,
  c: 1,
  u: 1,
  a: 1
}));
function $ct_sc_IndexedSeqView$IndexedSeqViewIterator__sc_IndexedSeqView__($thiz, self) {
  $thiz.id = self;
  $thiz.cE = 0;
  $thiz.b6 = self.q();
  return $thiz;
}
function $p_sc_IndexedSeqView$IndexedSeqViewIterator__formatRange$1__I__I($thiz, value) {
  return ((value < 0) ? 0 : ((value > $thiz.b6) ? $thiz.b6 : value));
}
/** @constructor */
function $c_sc_IndexedSeqView$IndexedSeqViewIterator() {
  this.id = null;
  this.cE = 0;
  this.b6 = 0;
}
$p = $c_sc_IndexedSeqView$IndexedSeqViewIterator.prototype = new $h_sc_AbstractIterator();
$p.constructor = $c_sc_IndexedSeqView$IndexedSeqViewIterator;
/** @constructor */
function $h_sc_IndexedSeqView$IndexedSeqViewIterator() {
}
$h_sc_IndexedSeqView$IndexedSeqViewIterator.prototype = $p;
$p.x = (function() {
  return this.b6;
});
$p.m = (function() {
  return (this.b6 > 0);
});
$p.g = (function() {
  if ((this.b6 > 0)) {
    var r = this.id.v(this.cE);
    this.cE = ((1 + this.cE) | 0);
    this.b6 = ((this.b6 - 1) | 0);
    return r;
  } else {
    return $m_sc_Iterator$().O.g();
  }
});
$p.dC = (function(n) {
  if ((n > 0)) {
    this.cE = ((this.cE + n) | 0);
    var b = ((this.b6 - n) | 0);
    this.b6 = ((b < 0) ? 0 : b);
  }
  return this;
});
$p.gg = (function(from, until) {
  var formatFrom = $p_sc_IndexedSeqView$IndexedSeqViewIterator__formatRange$1__I__I(this, from);
  var formatUntil = $p_sc_IndexedSeqView$IndexedSeqViewIterator__formatRange$1__I__I(this, until);
  var b = ((formatUntil - formatFrom) | 0);
  this.b6 = ((b < 0) ? 0 : b);
  this.cE = ((this.cE + formatFrom) | 0);
  return this;
});
var $d_sc_IndexedSeqView$IndexedSeqViewIterator = new $TypeData().i($c_sc_IndexedSeqView$IndexedSeqViewIterator, "scala.collection.IndexedSeqView$IndexedSeqViewIterator", ({
  bL: 1,
  t: 1,
  b: 1,
  c: 1,
  u: 1,
  a: 1
}));
/** @constructor */
function $c_sc_Iterator$$anon$21() {
  this.fG = null;
  $ct_scm_ImmutableBuilder__sc_IterableOnce__(this, $m_sc_Iterator$().O);
}
$p = $c_sc_Iterator$$anon$21.prototype = new $h_scm_ImmutableBuilder();
$p.constructor = $c_sc_Iterator$$anon$21;
/** @constructor */
function $h_sc_Iterator$$anon$21() {
}
$h_sc_Iterator$$anon$21.prototype = $p;
$p.oZ = (function(elem) {
  this.fG = this.fG.iO(new $c_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c((() => new $c_sc_Iterator$$anon$20(elem))));
  return this;
});
$p.aV = (function(elem) {
  return this.oZ(elem);
});
var $d_sc_Iterator$$anon$21 = new $TypeData().i($c_sc_Iterator$$anon$21, "scala.collection.Iterator$$anon$21", ({
  fu: 1,
  gS: 1,
  G: 1,
  I: 1,
  M: 1,
  a7: 1
}));
function $f_sc_MapOps__getOrElse__O__F0__O($thiz, key, default$1) {
  var x5 = $thiz.cr(key);
  if ((x5 instanceof $c_s_Some)) {
    return x5.cC;
  }
  if (($m_s_None$() === x5)) {
    return default$1.F();
  }
  throw new $c_s_MatchError(x5);
}
function $f_sc_MapOps__apply__O__O($thiz, key) {
  var x8 = $thiz.cr(key);
  if (($m_s_None$() === x8)) {
    return $thiz.nl(key);
  }
  if ((x8 instanceof $c_s_Some)) {
    return x8.cC;
  }
  throw new $c_s_MatchError(x8);
}
function $f_sc_MapOps__applyOrElse__O__F1__O($thiz, x, default$1) {
  return $thiz.c9(x, new $c_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c((() => default$1.b(x))));
}
function $f_sc_MapOps__foreachEntry__F2__V($thiz, f) {
  var it = $thiz.i();
  while (it.m()) {
    var next = it.g();
    f.eM(next.aZ, next.aQ);
  }
}
function $f_sc_MapOps__default__O__O($thiz, key) {
  throw $ct_ju_NoSuchElementException__T__(new $c_ju_NoSuchElementException(), ("key not found: " + key));
}
function $f_sc_MapOps__contains__O__Z($thiz, key) {
  return (!$thiz.cr(key).c());
}
function $f_sc_MapOps__addString__scm_StringBuilder__T__T__T__scm_StringBuilder($thiz, sb, start, sep, end) {
  return $f_sc_IterableOnceOps__addString__scm_StringBuilder__T__T__T__scm_StringBuilder(new $c_sc_Iterator$$anon$9(new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((x$1$2) => {
    var k = x$1$2.aZ;
    var v = x$1$2.aQ;
    return ((k + " -> ") + v);
  })), $thiz.i()), sb, start, sep, end);
}
function $f_sc_StrictOptimizedSeqOps__distinctBy__F1__O($thiz, f) {
  var builder = $thiz.g8();
  var seen = $ct_scm_HashSet__(new $c_scm_HashSet());
  var it = $thiz.i();
  while (it.m()) {
    var next = it.g();
    if (seen.gV(f.b(next))) {
      builder.aV(next);
    }
  }
  return builder.b2();
}
function $f_sc_StrictOptimizedSeqOps__appendedAll__sc_IterableOnce__O($thiz, suffix) {
  var b = $thiz.dD().aW();
  b.aU($thiz);
  b.aU(suffix);
  return b.b2();
}
function $p_sci_ArraySeq$__emptyImpl__sci_ArraySeq$ofRef($thiz) {
  if ((!$thiz.me)) {
    $thiz.md = new $c_sci_ArraySeq$ofRef(new ($d_sr_Nothing$.r().C)(0));
    $thiz.me = true;
  }
  return $thiz.md;
}
/** @constructor */
function $c_sci_ArraySeq$() {
  this.ih = null;
  this.md = null;
  this.me = false;
  $n_sci_ArraySeq$ = this;
  this.ih = new $c_sc_ClassTagSeqFactory$AnySeqDelegate(this);
}
$p = $c_sci_ArraySeq$.prototype = new $h_O();
$p.constructor = $c_sci_ArraySeq$;
/** @constructor */
function $h_sci_ArraySeq$() {
}
$h_sci_ArraySeq$.prototype = $p;
$p.j1 = (function(it, tag) {
  return ((it instanceof $c_sci_ArraySeq) ? it : this.ol($m_s_Array$().nu(it, tag)));
});
$p.hc = (function(evidence$1) {
  return new $c_scm_Builder$$anon$1(new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((b$2) => this.ol($f_sc_IterableOnceOps__toArray__s_reflect_ClassTag__O(b$2, evidence$1)))), ($m_scm_ArrayBuffer$(), new $c_scm_ArrayBuffer$$anon$1()));
});
$p.ol = (function(x) {
  if ((x === null)) {
    return null;
  }
  if ((x instanceof $ac_O)) {
    return new $c_sci_ArraySeq$ofRef(x);
  }
  if ((x instanceof $ac_I)) {
    return new $c_sci_ArraySeq$ofInt(x);
  }
  if ((x instanceof $ac_D)) {
    return new $c_sci_ArraySeq$ofDouble(x);
  }
  if ((x instanceof $ac_J)) {
    return new $c_sci_ArraySeq$ofLong(x);
  }
  if ((x instanceof $ac_F)) {
    return new $c_sci_ArraySeq$ofFloat(x);
  }
  if ((x instanceof $ac_C)) {
    return new $c_sci_ArraySeq$ofChar(x);
  }
  if ((x instanceof $ac_B)) {
    return new $c_sci_ArraySeq$ofByte(x);
  }
  if ((x instanceof $ac_S)) {
    return new $c_sci_ArraySeq$ofShort(x);
  }
  if ((x instanceof $ac_Z)) {
    return new $c_sci_ArraySeq$ofBoolean(x);
  }
  if ($isArrayOf_jl_Void(x, 1)) {
    return new $c_sci_ArraySeq$ofUnit(x);
  }
  throw new $c_s_MatchError(x);
});
$p.j0 = (function(it, evidence$1) {
  return this.j1(it, evidence$1);
});
var $d_sci_ArraySeq$ = new $TypeData().i($c_sci_ArraySeq$, "scala.collection.immutable.ArraySeq$", ({
  fL: 1,
  a: 1,
  bJ: 1,
  bH: 1,
  bI: 1,
  bP: 1
}));
var $n_sci_ArraySeq$;
function $m_sci_ArraySeq$() {
  if ((!$n_sci_ArraySeq$)) {
    $n_sci_ArraySeq$ = new $c_sci_ArraySeq$();
  }
  return $n_sci_ArraySeq$;
}
/** @constructor */
function $c_sci_HashMapBuilder$$anon$1(hm$1, outer) {
  this.bB = 0;
  this.fw = 0;
  this.dT = null;
  this.bu = 0;
  this.cH = null;
  this.fx = null;
  if ((outer === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
  $ct_sci_ChampBaseIterator__sci_Node__(this, hm$1.b7);
  while (this.m()) {
    var originalHash = this.dT.g3(this.bB);
    outer.eY(outer.cg, this.dT.cW(this.bB), this.dT.ct(this.bB), originalHash, $m_sc_Hashing$().c0(originalHash), 0);
    this.bB = ((1 + this.bB) | 0);
  }
}
$p = $c_sci_HashMapBuilder$$anon$1.prototype = new $h_sci_ChampBaseIterator();
$p.constructor = $c_sci_HashMapBuilder$$anon$1;
/** @constructor */
function $h_sci_HashMapBuilder$$anon$1() {
}
$h_sci_HashMapBuilder$$anon$1.prototype = $p;
$p.g = (function() {
  return $m_sc_Iterator$().O.g();
});
var $d_sci_HashMapBuilder$$anon$1 = new $TypeData().i($c_sci_HashMapBuilder$$anon$1, "scala.collection.immutable.HashMapBuilder$$anon$1", ({
  fP: 1,
  c2: 1,
  t: 1,
  b: 1,
  c: 1,
  u: 1
}));
function $is_sci_Iterable(obj) {
  return (!(!((obj && obj.$classData) && obj.$classData.n.r)));
}
function $isArrayOf_sci_Iterable(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.r)));
}
/** @constructor */
function $c_sci_Map$Map2$$anon$1(outer) {
  this.df = 0;
  this.eA = null;
  if ((outer === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
  $ct_sci_Map$Map2$Map2Iterator__sci_Map$Map2__(this, outer);
}
$p = $c_sci_Map$Map2$$anon$1.prototype = new $h_sci_Map$Map2$Map2Iterator();
$p.constructor = $c_sci_Map$Map2$$anon$1;
/** @constructor */
function $h_sci_Map$Map2$$anon$1() {
}
$h_sci_Map$Map2$$anon$1.prototype = $p;
var $d_sci_Map$Map2$$anon$1 = new $TypeData().i($c_sci_Map$Map2$$anon$1, "scala.collection.immutable.Map$Map2$$anon$1", ({
  g4: 1,
  g5: 1,
  t: 1,
  b: 1,
  c: 1,
  u: 1
}));
/** @constructor */
function $c_sci_Map$Map3$$anon$4(outer) {
  this.dh = 0;
  this.dg = null;
  if ((outer === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
  $ct_sci_Map$Map3$Map3Iterator__sci_Map$Map3__(this, outer);
}
$p = $c_sci_Map$Map3$$anon$4.prototype = new $h_sci_Map$Map3$Map3Iterator();
$p.constructor = $c_sci_Map$Map3$$anon$4;
/** @constructor */
function $h_sci_Map$Map3$$anon$4() {
}
$h_sci_Map$Map3$$anon$4.prototype = $p;
var $d_sci_Map$Map3$$anon$4 = new $TypeData().i($c_sci_Map$Map3$$anon$4, "scala.collection.immutable.Map$Map3$$anon$4", ({
  g6: 1,
  g7: 1,
  t: 1,
  b: 1,
  c: 1,
  u: 1
}));
/** @constructor */
function $c_sci_Map$Map4$$anon$7(outer) {
  this.di = 0;
  this.cl = null;
  if ((outer === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
  $ct_sci_Map$Map4$Map4Iterator__sci_Map$Map4__(this, outer);
}
$p = $c_sci_Map$Map4$$anon$7.prototype = new $h_sci_Map$Map4$Map4Iterator();
$p.constructor = $c_sci_Map$Map4$$anon$7;
/** @constructor */
function $h_sci_Map$Map4$$anon$7() {
}
$h_sci_Map$Map4$$anon$7.prototype = $p;
var $d_sci_Map$Map4$$anon$7 = new $TypeData().i($c_sci_Map$Map4$$anon$7, "scala.collection.immutable.Map$Map4$$anon$7", ({
  g8: 1,
  g9: 1,
  t: 1,
  b: 1,
  c: 1,
  u: 1
}));
/** @constructor */
function $c_sci_MapKeyValueTupleHashIterator(rootNode) {
  this.dc = 0;
  this.gJ = null;
  this.bC = 0;
  this.fy = null;
  this.fz = null;
  this.il = 0;
  this.mh = null;
  $ct_sci_ChampBaseReverseIterator__sci_Node__(this, rootNode);
  this.il = 0;
}
$p = $c_sci_MapKeyValueTupleHashIterator.prototype = new $h_sci_ChampBaseReverseIterator();
$p.constructor = $c_sci_MapKeyValueTupleHashIterator;
/** @constructor */
function $h_sci_MapKeyValueTupleHashIterator() {
}
$h_sci_MapKeyValueTupleHashIterator.prototype = $p;
$p.r = (function() {
  return $m_s_util_hashing_MurmurHash3$().ok(this.il, $m_sr_Statics$().C(this.mh), (-889275714));
});
$p.qH = (function() {
  if ((!this.m())) {
    $m_sc_Iterator$().O.g();
  }
  this.il = this.gJ.g3(this.dc);
  this.mh = this.gJ.ct(this.dc);
  this.dc = ((this.dc - 1) | 0);
  return this;
});
$p.g = (function() {
  return this.qH();
});
var $d_sci_MapKeyValueTupleHashIterator = new $TypeData().i($c_sci_MapKeyValueTupleHashIterator, "scala.collection.immutable.MapKeyValueTupleHashIterator", ({
  gc: 1,
  fM: 1,
  t: 1,
  b: 1,
  c: 1,
  u: 1
}));
/** @constructor */
function $c_sci_MapKeyValueTupleIterator(rootNode) {
  this.bB = 0;
  this.fw = 0;
  this.dT = null;
  this.bu = 0;
  this.cH = null;
  this.fx = null;
  $ct_sci_ChampBaseIterator__sci_Node__(this, rootNode);
}
$p = $c_sci_MapKeyValueTupleIterator.prototype = new $h_sci_ChampBaseIterator();
$p.constructor = $c_sci_MapKeyValueTupleIterator;
/** @constructor */
function $h_sci_MapKeyValueTupleIterator() {
}
$h_sci_MapKeyValueTupleIterator.prototype = $p;
$p.qG = (function() {
  if ((!this.m())) {
    $m_sc_Iterator$().O.g();
  }
  var payload = this.dT.nD(this.bB);
  this.bB = ((1 + this.bB) | 0);
  return payload;
});
$p.g = (function() {
  return this.qG();
});
var $d_sci_MapKeyValueTupleIterator = new $TypeData().i($c_sci_MapKeyValueTupleIterator, "scala.collection.immutable.MapKeyValueTupleIterator", ({
  gd: 1,
  c2: 1,
  t: 1,
  b: 1,
  c: 1,
  u: 1
}));
function $p_sci_NewVectorIterator__advanceSlice__V($thiz) {
  if (($thiz.bv <= $thiz.ai)) {
    $m_sc_Iterator$().O.g();
  }
  $thiz.dl = ((1 + $thiz.dl) | 0);
  var slice = $thiz.io.cw($thiz.dl);
  while ((slice.a.length === 0)) {
    $thiz.dl = ((1 + $thiz.dl) | 0);
    slice = $thiz.io.cw($thiz.dl);
  }
  $thiz.fB = $thiz.dW;
  var count = $thiz.mj;
  var idx = $thiz.dl;
  var c = (((count + ((count >>> 31) | 0)) | 0) >> 1);
  var a = ((idx - c) | 0);
  var sign = (a >> 31);
  $thiz.dk = ((((1 + c) | 0) - (((a ^ sign) - sign) | 0)) | 0);
  var x46 = $thiz.dk;
  switch (x46) {
    case 1: {
      $thiz.aF = slice;
      break;
    }
    case 2: {
      $thiz.aG = slice;
      break;
    }
    case 3: {
      $thiz.bi = slice;
      break;
    }
    case 4: {
      $thiz.c6 = slice;
      break;
    }
    case 5: {
      $thiz.dV = slice;
      break;
    }
    case 6: {
      $thiz.im = slice;
      break;
    }
    default: {
      throw new $c_s_MatchError(x46);
    }
  }
  $thiz.dW = (($thiz.fB + Math.imul(slice.a.length, (1 << Math.imul(5, (($thiz.dk - 1) | 0))))) | 0);
  if (($thiz.dW > $thiz.cM)) {
    $thiz.dW = $thiz.cM;
  }
  if (($thiz.dk > 1)) {
    $thiz.eB = (((1 << Math.imul(5, $thiz.dk)) - 1) | 0);
  }
}
function $p_sci_NewVectorIterator__advance__V($thiz) {
  var pos = (((($thiz.ai - $thiz.bv) | 0) + $thiz.cM) | 0);
  if ((pos === $thiz.dW)) {
    $p_sci_NewVectorIterator__advanceSlice__V($thiz);
  }
  if (($thiz.dk > 1)) {
    var io = ((pos - $thiz.fB) | 0);
    $p_sci_NewVectorIterator__advanceA__I__I__V($thiz, io, ($thiz.eB ^ io));
    $thiz.eB = io;
  }
  $thiz.bv = (($thiz.bv - $thiz.ai) | 0);
  var a = $thiz.aF.a.length;
  var b = $thiz.bv;
  $thiz.cL = ((a < b) ? a : b);
  $thiz.ai = 0;
}
function $p_sci_NewVectorIterator__advanceA__I__I__V($thiz, io, xor) {
  if ((xor < 1024)) {
    $thiz.aF = $thiz.aG.a[(31 & ((io >>> 5) | 0))];
  } else if ((xor < 32768)) {
    $thiz.aG = $thiz.bi.a[(31 & ((io >>> 10) | 0))];
    $thiz.aF = $thiz.aG.a[0];
  } else if ((xor < 1048576)) {
    $thiz.bi = $thiz.c6.a[(31 & ((io >>> 15) | 0))];
    $thiz.aG = $thiz.bi.a[0];
    $thiz.aF = $thiz.aG.a[0];
  } else if ((xor < 33554432)) {
    $thiz.c6 = $thiz.dV.a[(31 & ((io >>> 20) | 0))];
    $thiz.bi = $thiz.c6.a[0];
    $thiz.aG = $thiz.bi.a[0];
    $thiz.aF = $thiz.aG.a[0];
  } else {
    $thiz.dV = $thiz.im.a[((io >>> 25) | 0)];
    $thiz.c6 = $thiz.dV.a[0];
    $thiz.bi = $thiz.c6.a[0];
    $thiz.aG = $thiz.bi.a[0];
    $thiz.aF = $thiz.aG.a[0];
  }
}
function $p_sci_NewVectorIterator__setA__I__I__V($thiz, io, xor) {
  if ((xor < 1024)) {
    $thiz.aF = $thiz.aG.a[(31 & ((io >>> 5) | 0))];
  } else if ((xor < 32768)) {
    $thiz.aG = $thiz.bi.a[(31 & ((io >>> 10) | 0))];
    $thiz.aF = $thiz.aG.a[(31 & ((io >>> 5) | 0))];
  } else if ((xor < 1048576)) {
    $thiz.bi = $thiz.c6.a[(31 & ((io >>> 15) | 0))];
    $thiz.aG = $thiz.bi.a[(31 & ((io >>> 10) | 0))];
    $thiz.aF = $thiz.aG.a[(31 & ((io >>> 5) | 0))];
  } else if ((xor < 33554432)) {
    $thiz.c6 = $thiz.dV.a[(31 & ((io >>> 20) | 0))];
    $thiz.bi = $thiz.c6.a[(31 & ((io >>> 15) | 0))];
    $thiz.aG = $thiz.bi.a[(31 & ((io >>> 10) | 0))];
    $thiz.aF = $thiz.aG.a[(31 & ((io >>> 5) | 0))];
  } else {
    $thiz.dV = $thiz.im.a[((io >>> 25) | 0)];
    $thiz.c6 = $thiz.dV.a[(31 & ((io >>> 20) | 0))];
    $thiz.bi = $thiz.c6.a[(31 & ((io >>> 15) | 0))];
    $thiz.aG = $thiz.bi.a[(31 & ((io >>> 10) | 0))];
    $thiz.aF = $thiz.aG.a[(31 & ((io >>> 5) | 0))];
  }
}
/** @constructor */
function $c_sci_NewVectorIterator(v, totalLength, sliceCount) {
  this.io = null;
  this.cM = 0;
  this.mj = 0;
  this.aF = null;
  this.aG = null;
  this.bi = null;
  this.c6 = null;
  this.dV = null;
  this.im = null;
  this.cL = 0;
  this.ai = 0;
  this.eB = 0;
  this.bv = 0;
  this.dl = 0;
  this.dk = 0;
  this.fB = 0;
  this.dW = 0;
  this.io = v;
  this.cM = totalLength;
  this.mj = sliceCount;
  this.aF = v.d;
  this.cL = this.aF.a.length;
  this.ai = 0;
  this.eB = 0;
  this.bv = this.cM;
  this.dl = 0;
  this.dk = 1;
  this.fB = 0;
  this.dW = this.cL;
}
$p = $c_sci_NewVectorIterator.prototype = new $h_sc_AbstractIterator();
$p.constructor = $c_sci_NewVectorIterator;
/** @constructor */
function $h_sci_NewVectorIterator() {
}
$h_sci_NewVectorIterator.prototype = $p;
$p.x = (function() {
  return ((this.bv - this.ai) | 0);
});
$p.m = (function() {
  return (this.bv > this.ai);
});
$p.g = (function() {
  if ((this.ai === this.cL)) {
    $p_sci_NewVectorIterator__advance__V(this);
  }
  var r = this.aF.a[this.ai];
  this.ai = ((1 + this.ai) | 0);
  return r;
});
$p.dC = (function(n) {
  if ((n > 0)) {
    var oldpos = ((((this.ai - this.bv) | 0) + this.cM) | 0);
    var a = ((oldpos + n) | 0);
    var b = this.cM;
    var newpos = ((a < b) ? a : b);
    if ((newpos === this.cM)) {
      this.ai = 0;
      this.bv = 0;
      this.cL = 0;
    } else {
      while ((newpos >= this.dW)) {
        $p_sci_NewVectorIterator__advanceSlice__V(this);
      }
      var io = ((newpos - this.fB) | 0);
      if ((this.dk > 1)) {
        $p_sci_NewVectorIterator__setA__I__I__V(this, io, (this.eB ^ io));
        this.eB = io;
      }
      this.cL = this.aF.a.length;
      this.ai = (31 & io);
      this.bv = ((this.ai + ((this.cM - newpos) | 0)) | 0);
      if ((this.cL > this.bv)) {
        this.cL = this.bv;
      }
    }
  }
  return this;
});
$p.bI = (function(xs, start, len) {
  var xsLen = $m_jl_reflect_Array$().bJ(xs);
  var srcLen = ((this.bv - this.ai) | 0);
  var limit = ((len < srcLen) ? len : srcLen);
  var capacity = ((start < 0) ? xsLen : ((xsLen - start) | 0));
  var total = ((capacity < limit) ? capacity : limit);
  var total$1 = ((total < 0) ? 0 : total);
  var copied = 0;
  var isBoxed = (xs instanceof $ac_O);
  while ((copied < total$1)) {
    if ((this.ai === this.cL)) {
      $p_sci_NewVectorIterator__advance__V(this);
    }
    var a = ((total$1 - copied) | 0);
    var b = ((this.aF.a.length - this.ai) | 0);
    var count = ((a < b) ? a : b);
    if (isBoxed) {
      var src = this.aF;
      var srcPos = this.ai;
      var destPos = ((start + copied) | 0);
      src.u(srcPos, xs, destPos, count);
    } else {
      $m_s_Array$().fZ(this.aF, this.ai, xs, ((start + copied) | 0), count);
    }
    this.ai = ((this.ai + count) | 0);
    copied = ((copied + count) | 0);
  }
  return total$1;
});
var $d_sci_NewVectorIterator = new $TypeData().i($c_sci_NewVectorIterator, "scala.collection.immutable.NewVectorIterator", ({
  gf: 1,
  t: 1,
  b: 1,
  c: 1,
  u: 1,
  A: 1
}));
function $ct_scm_ArrayBuilder__($thiz) {
  $thiz.is = 0;
  $thiz.mp = 0;
  return $thiz;
}
/** @constructor */
function $c_scm_ArrayBuilder() {
  this.is = 0;
  this.mp = 0;
}
$p = $c_scm_ArrayBuilder.prototype = new $h_O();
$p.constructor = $c_scm_ArrayBuilder;
/** @constructor */
function $h_scm_ArrayBuilder() {
}
$h_scm_ArrayBuilder.prototype = $p;
$p.aX = (function(size) {
  if ((this.is < size)) {
    this.r4(size);
  }
});
/** @constructor */
function $c_scm_ArraySeq$() {
  this.iu = null;
  this.mr = null;
  $n_scm_ArraySeq$ = this;
  this.iu = new $c_sc_ClassTagSeqFactory$AnySeqDelegate(this);
  this.mr = new $c_scm_ArraySeq$ofRef(new $ac_O(0));
}
$p = $c_scm_ArraySeq$.prototype = new $h_O();
$p.constructor = $c_scm_ArraySeq$;
/** @constructor */
function $h_scm_ArraySeq$() {
}
$h_scm_ArraySeq$.prototype = $p;
$p.q1 = (function(it, evidence$1) {
  return this.jf($m_s_Array$().nu(it, evidence$1));
});
$p.hc = (function(evidence$1) {
  return new $c_scm_Builder$$anon$1(new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((x$2) => this.jf(x$2))), new $c_scm_ArrayBuilder$generic(evidence$1.aC()));
});
$p.jf = (function(x) {
  if ((x === null)) {
    return null;
  }
  if ((x instanceof $ac_O)) {
    return new $c_scm_ArraySeq$ofRef(x);
  }
  if ((x instanceof $ac_I)) {
    return new $c_scm_ArraySeq$ofInt(x);
  }
  if ((x instanceof $ac_D)) {
    return new $c_scm_ArraySeq$ofDouble(x);
  }
  if ((x instanceof $ac_J)) {
    return new $c_scm_ArraySeq$ofLong(x);
  }
  if ((x instanceof $ac_F)) {
    return new $c_scm_ArraySeq$ofFloat(x);
  }
  if ((x instanceof $ac_C)) {
    return new $c_scm_ArraySeq$ofChar(x);
  }
  if ((x instanceof $ac_B)) {
    return new $c_scm_ArraySeq$ofByte(x);
  }
  if ((x instanceof $ac_S)) {
    return new $c_scm_ArraySeq$ofShort(x);
  }
  if ((x instanceof $ac_Z)) {
    return new $c_scm_ArraySeq$ofBoolean(x);
  }
  if ($isArrayOf_jl_Void(x, 1)) {
    return new $c_scm_ArraySeq$ofUnit(x);
  }
  throw new $c_s_MatchError(x);
});
$p.j0 = (function(it, evidence$1) {
  return this.q1(it, evidence$1);
});
var $d_scm_ArraySeq$ = new $TypeData().i($c_scm_ArraySeq$, "scala.collection.mutable.ArraySeq$", ({
  gH: 1,
  a: 1,
  bJ: 1,
  bH: 1,
  bI: 1,
  bP: 1
}));
var $n_scm_ArraySeq$;
function $m_scm_ArraySeq$() {
  if ((!$n_scm_ArraySeq$)) {
    $n_scm_ArraySeq$ = new $c_scm_ArraySeq$();
  }
  return $n_scm_ArraySeq$;
}
/** @constructor */
function $c_scm_HashSet$$anon$1(outer) {
  this.du = 0;
  this.cP = null;
  this.fF = 0;
  this.fE = null;
  if ((outer === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
  $ct_scm_HashSet$HashSetIterator__scm_HashSet__(this, outer);
}
$p = $c_scm_HashSet$$anon$1.prototype = new $h_scm_HashSet$HashSetIterator();
$p.constructor = $c_scm_HashSet$$anon$1;
/** @constructor */
function $h_scm_HashSet$$anon$1() {
}
$h_scm_HashSet$$anon$1.prototype = $p;
$p.iX = (function(nd) {
  return nd.eF;
});
var $d_scm_HashSet$$anon$1 = new $TypeData().i($c_scm_HashSet$$anon$1, "scala.collection.mutable.HashSet$$anon$1", ({
  gN: 1,
  aV: 1,
  t: 1,
  b: 1,
  c: 1,
  u: 1
}));
/** @constructor */
function $c_scm_HashSet$$anon$2(outer) {
  this.du = 0;
  this.cP = null;
  this.fF = 0;
  this.fE = null;
  if ((outer === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
  $ct_scm_HashSet$HashSetIterator__scm_HashSet__(this, outer);
}
$p = $c_scm_HashSet$$anon$2.prototype = new $h_scm_HashSet$HashSetIterator();
$p.constructor = $c_scm_HashSet$$anon$2;
/** @constructor */
function $h_scm_HashSet$$anon$2() {
}
$h_scm_HashSet$$anon$2.prototype = $p;
$p.iX = (function(nd) {
  return nd;
});
var $d_scm_HashSet$$anon$2 = new $TypeData().i($c_scm_HashSet$$anon$2, "scala.collection.mutable.HashSet$$anon$2", ({
  gO: 1,
  aV: 1,
  t: 1,
  b: 1,
  c: 1,
  u: 1
}));
/** @constructor */
function $c_scm_HashSet$$anon$3(outer) {
  this.du = 0;
  this.cP = null;
  this.fF = 0;
  this.fE = null;
  this.ix = 0;
  this.mv = null;
  if ((outer === null)) {
    throw $ct_jl_NullPointerException__(new $c_jl_NullPointerException());
  }
  this.mv = outer;
  $ct_scm_HashSet$HashSetIterator__scm_HashSet__(this, outer);
  this.ix = 0;
}
$p = $c_scm_HashSet$$anon$3.prototype = new $h_scm_HashSet$HashSetIterator();
$p.constructor = $c_scm_HashSet$$anon$3;
/** @constructor */
function $h_scm_HashSet$$anon$3() {
}
$h_scm_HashSet$$anon$3.prototype = $p;
$p.r = (function() {
  return this.ix;
});
$p.iX = (function(nd) {
  this.ix = $p_scm_HashSet__improveHash__I__I(this.mv, nd.cQ);
  return this;
});
var $d_scm_HashSet$$anon$3 = new $TypeData().i($c_scm_HashSet$$anon$3, "scala.collection.mutable.HashSet$$anon$3", ({
  gP: 1,
  aV: 1,
  t: 1,
  b: 1,
  c: 1,
  u: 1
}));
/** @constructor */
function $c_s_reflect_ClassTag$GenericClassTag(runtimeClass) {
  this.fN = null;
  this.fN = runtimeClass;
}
$p = $c_s_reflect_ClassTag$GenericClassTag.prototype = new $h_O();
$p.constructor = $c_s_reflect_ClassTag$GenericClassTag;
/** @constructor */
function $h_s_reflect_ClassTag$GenericClassTag() {
}
$h_s_reflect_ClassTag$GenericClassTag.prototype = $p;
$p.k = (function(x) {
  return $f_s_reflect_ClassTag__equals__O__Z(this, x);
});
$p.r = (function() {
  return $m_sr_Statics$().C(this.fN);
});
$p.t = (function() {
  return $p_s_reflect_ClassTag__prettyprint$1__jl_Class__T(this, this.fN);
});
$p.aC = (function() {
  return this.fN;
});
$p.bo = (function(len) {
  return this.fN.ah.U(len);
});
var $d_s_reflect_ClassTag$GenericClassTag = new $TypeData().i($c_s_reflect_ClassTag$GenericClassTag, "scala.reflect.ClassTag$GenericClassTag", ({
  hi: 1,
  a: 1,
  Q: 1,
  P: 1,
  d: 1,
  F: 1
}));
function $ct_Ljava_io_PrintStream__Ljava_io_OutputStream__Z__Ljava_nio_charset_Charset__($thiz, _out, autoFlush, charset) {
  $ct_Ljava_io_FilterOutputStream__Ljava_io_OutputStream__($thiz, _out);
  return $thiz;
}
/** @constructor */
function $c_Ljava_io_PrintStream() {
}
$p = $c_Ljava_io_PrintStream.prototype = new $h_Ljava_io_FilterOutputStream();
$p.constructor = $c_Ljava_io_PrintStream;
/** @constructor */
function $h_Ljava_io_PrintStream() {
}
$h_Ljava_io_PrintStream.prototype = $p;
$p.e6 = (function(s) {
  this.qP(s);
  this.nK("\n");
});
function $f_sc_View__toString__T($thiz) {
  return ($thiz.bZ() + "(<not computed>)");
}
function $is_sc_View(obj) {
  return (!(!((obj && obj.$classData) && obj.$classData.n.ac)));
}
function $isArrayOf_sc_View(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.ac)));
}
/** @constructor */
function $c_scm_ArrayBuilder$generic(elementClass) {
  this.is = 0;
  this.mp = 0;
  this.eE = null;
  this.mq = false;
  this.it = null;
  this.eE = elementClass;
  $ct_scm_ArrayBuilder__(this);
  this.mq = (elementClass === $d_C.l());
  this.it = [];
}
$p = $c_scm_ArrayBuilder$generic.prototype = new $h_scm_ArrayBuilder();
$p.constructor = $c_scm_ArrayBuilder$generic;
/** @constructor */
function $h_scm_ArrayBuilder$generic() {
}
$h_scm_ArrayBuilder$generic.prototype = $p;
$p.n2 = (function(elem) {
  var unboxedElem = (this.mq ? $uC(elem) : ((elem === null) ? $m_scm_ArrayBuilder$().hk(this.eE) : elem));
  this.it.push(unboxedElem);
  return this;
});
$p.oS = (function(xs) {
  var it = xs.i();
  while (it.m()) {
    this.n2(it.g());
  }
  return this;
});
$p.r4 = (function(size) {
});
$p.b2 = (function() {
  return $m_scm_ArrayBuilder$().hj(((this.eE === $d_V.l()) ? $d_jl_Void.l() : (((this.eE === $d_sr_Null$.l()) || (this.eE === $d_sr_Nothing$.l())) ? $d_O.l() : this.eE)), this.it);
});
$p.t = (function() {
  return "ArrayBuilder.generic";
});
$p.aV = (function(elem) {
  return this.n2(elem);
});
$p.aU = (function(elems) {
  return this.oS(elems);
});
var $d_scm_ArrayBuilder$generic = new $TypeData().i($c_scm_ArrayBuilder$generic, "scala.collection.mutable.ArrayBuilder$generic", ({
  gG: 1,
  gE: 1,
  G: 1,
  I: 1,
  M: 1,
  a7: 1,
  a: 1
}));
/** @constructor */
function $c_scm_CheckedIndexedSeqView$CheckedIterator(self, mutationCount) {
  this.id = null;
  this.cE = 0;
  this.b6 = 0;
  this.mu = null;
  this.mt = 0;
  this.mu = mutationCount;
  $ct_sc_IndexedSeqView$IndexedSeqViewIterator__sc_IndexedSeqView__(this, self);
  this.mt = (mutationCount.F() | 0);
}
$p = $c_scm_CheckedIndexedSeqView$CheckedIterator.prototype = new $h_sc_IndexedSeqView$IndexedSeqViewIterator();
$p.constructor = $c_scm_CheckedIndexedSeqView$CheckedIterator;
/** @constructor */
function $h_scm_CheckedIndexedSeqView$CheckedIterator() {
}
$h_scm_CheckedIndexedSeqView$CheckedIterator.prototype = $p;
$p.m = (function() {
  $m_scm_MutationTracker$().nd(this.mt, (this.mu.F() | 0), "mutation occurred during iteration");
  return (this.b6 > 0);
});
var $d_scm_CheckedIndexedSeqView$CheckedIterator = new $TypeData().i($c_scm_CheckedIndexedSeqView$CheckedIterator, "scala.collection.mutable.CheckedIndexedSeqView$CheckedIterator", ({
  gK: 1,
  bL: 1,
  t: 1,
  b: 1,
  c: 1,
  u: 1,
  a: 1
}));
class $c_s_concurrent_Future$$anon$1 extends $c_ju_NoSuchElementException {
  constructor(t$2) {
    super();
    $ct_jl_Throwable__T__jl_Throwable__Z__Z__(this, ("Future.collect partial function is not defined at: " + t$2), null, true, true);
  }
  eP() {
    return $f_s_util_control_NoStackTrace__fillInStackTrace__jl_Throwable(this);
  }
}
var $d_s_concurrent_Future$$anon$1 = new $TypeData().i($c_s_concurrent_Future$$anon$1, "scala.concurrent.Future$$anon$1", ({
  h8: 1,
  at: 1,
  D: 1,
  B: 1,
  s: 1,
  a: 1,
  ay: 1
}));
class $c_s_concurrent_Future$$anon$2 extends $c_ju_NoSuchElementException {
  constructor() {
    super();
    $ct_jl_Throwable__T__jl_Throwable__Z__Z__(this, "Future.filter predicate is not satisfied", null, true, true);
  }
  eP() {
    return $f_s_util_control_NoStackTrace__fillInStackTrace__jl_Throwable(this);
  }
}
var $d_s_concurrent_Future$$anon$2 = new $TypeData().i($c_s_concurrent_Future$$anon$2, "scala.concurrent.Future$$anon$2", ({
  h9: 1,
  at: 1,
  D: 1,
  B: 1,
  s: 1,
  a: 1,
  ay: 1
}));
class $c_s_concurrent_Future$$anon$3 extends $c_ju_NoSuchElementException {
  constructor() {
    super();
    $ct_jl_Throwable__T__jl_Throwable__Z__Z__(this, "Future.failed not completed with a throwable.", null, true, true);
  }
  eP() {
    return $f_s_util_control_NoStackTrace__fillInStackTrace__jl_Throwable(this);
  }
}
var $d_s_concurrent_Future$$anon$3 = new $TypeData().i($c_s_concurrent_Future$$anon$3, "scala.concurrent.Future$$anon$3", ({
  ha: 1,
  at: 1,
  D: 1,
  B: 1,
  s: 1,
  a: 1,
  ay: 1
}));
function $ct_s_concurrent_impl_Promise$DefaultPromise__O__($thiz, initial) {
  $ct_ju_concurrent_atomic_AtomicReference__O__($thiz, initial);
  return $thiz;
}
function $ct_s_concurrent_impl_Promise$DefaultPromise__s_util_Try__($thiz, result) {
  $ct_s_concurrent_impl_Promise$DefaultPromise__O__($thiz, $m_s_concurrent_impl_Promise$().gd(result));
  return $thiz;
}
function $ct_s_concurrent_impl_Promise$DefaultPromise__($thiz) {
  $ct_s_concurrent_impl_Promise$DefaultPromise__O__($thiz, $m_s_concurrent_impl_Promise$().fJ);
  return $thiz;
}
function $p_s_concurrent_impl_Promise$DefaultPromise__value0__s_util_Try($thiz) {
  var \u03b4this$tailLocal2 = $thiz;
  while (true) {
    var state = \u03b4this$tailLocal2.L;
    if ((state instanceof $c_s_util_Try)) {
      return state;
    } else if ((state instanceof $c_s_concurrent_impl_Promise$Link)) {
      \u03b4this$tailLocal2 = state.eV(\u03b4this$tailLocal2);
    } else {
      return null;
    }
  }
}
function $p_s_concurrent_impl_Promise$DefaultPromise__dispatchOrAddCallbacks__O__s_concurrent_impl_Promise$Callbacks__s_concurrent_impl_Promise$Callbacks($thiz, state, callbacks) {
  var \u03b4this$tailLocal4 = $thiz;
  var state$tailLocal2 = state;
  while (true) {
    if ((state$tailLocal2 instanceof $c_s_util_Try)) {
      $p_s_concurrent_impl_Promise$DefaultPromise__submitWithValue__s_concurrent_impl_Promise$Callbacks__s_util_Try__V(\u03b4this$tailLocal4, callbacks, state$tailLocal2);
      return callbacks;
    } else if ($is_s_concurrent_impl_Promise$Callbacks(state$tailLocal2)) {
      if (\u03b4this$tailLocal4.fY(state$tailLocal2, ((state$tailLocal2 !== $m_s_concurrent_impl_Promise$().fJ) ? $p_s_concurrent_impl_Promise$DefaultPromise__concatCallbacks__s_concurrent_impl_Promise$Callbacks__s_concurrent_impl_Promise$Callbacks__s_concurrent_impl_Promise$Callbacks(\u03b4this$tailLocal4, callbacks, state$tailLocal2) : callbacks))) {
        return callbacks;
      } else {
        state$tailLocal2 = \u03b4this$tailLocal4.L;
      }
    } else {
      var p = state$tailLocal2.eV(\u03b4this$tailLocal4);
      var state$tailLocal2$tmp1 = p.L;
      \u03b4this$tailLocal4 = p;
      state$tailLocal2 = state$tailLocal2$tmp1;
    }
  }
}
function $p_s_concurrent_impl_Promise$DefaultPromise__concatCallbacks__s_concurrent_impl_Promise$Callbacks__s_concurrent_impl_Promise$Callbacks__s_concurrent_impl_Promise$Callbacks($thiz, left, right) {
  var right$tailLocal1 = right;
  var left$tailLocal1 = left;
  while (true) {
    if ((left$tailLocal1 instanceof $c_s_concurrent_impl_Promise$Transformation)) {
      return new $c_s_concurrent_impl_Promise$ManyCallbacks(left$tailLocal1, right$tailLocal1);
    } else {
      var m = left$tailLocal1;
      var left$tailLocal1$tmp1 = m.iB;
      var right$tailLocal1$tmp1 = new $c_s_concurrent_impl_Promise$ManyCallbacks(m.iA, right$tailLocal1);
      left$tailLocal1 = left$tailLocal1$tmp1;
      right$tailLocal1 = right$tailLocal1$tmp1;
    }
  }
}
function $p_s_concurrent_impl_Promise$DefaultPromise__submitWithValue__s_concurrent_impl_Promise$Callbacks__s_util_Try__V($thiz, callbacks, resolved) {
  var callbacks$tailLocal1 = callbacks;
  while (true) {
    if ((callbacks$tailLocal1 instanceof $c_s_concurrent_impl_Promise$ManyCallbacks)) {
      var m = callbacks$tailLocal1;
      m.iA.of(resolved);
      callbacks$tailLocal1 = m.iB;
    } else {
      callbacks$tailLocal1.of(resolved);
      return (void 0);
    }
  }
}
/** @constructor */
function $c_s_concurrent_impl_Promise$DefaultPromise() {
  this.L = null;
}
$p = $c_s_concurrent_impl_Promise$DefaultPromise.prototype = new $h_ju_concurrent_atomic_AtomicReference();
$p.constructor = $c_s_concurrent_impl_Promise$DefaultPromise;
/** @constructor */
function $h_s_concurrent_impl_Promise$DefaultPromise() {
}
$h_s_concurrent_impl_Promise$DefaultPromise.prototype = $p;
$p.iY = (function(f, executor) {
  var state = this.L;
  return ((!(state instanceof $c_s_util_Failure)) ? $p_s_concurrent_impl_Promise$DefaultPromise__dispatchOrAddCallbacks__O__s_concurrent_impl_Promise$Callbacks__s_concurrent_impl_Promise$Callbacks(this, state, $ct_s_concurrent_impl_Promise$Transformation__I__F1__s_concurrent_ExecutionContext__(new $c_s_concurrent_impl_Promise$Transformation(), 2, f, executor)) : this);
});
$p.qz = (function(f, executor) {
  var state = this.L;
  return ((!(state instanceof $c_s_util_Failure)) ? $p_s_concurrent_impl_Promise$DefaultPromise__dispatchOrAddCallbacks__O__s_concurrent_impl_Promise$Callbacks__s_concurrent_impl_Promise$Callbacks(this, state, $ct_s_concurrent_impl_Promise$Transformation__I__F1__s_concurrent_ExecutionContext__(new $c_s_concurrent_impl_Promise$Transformation(), 1, f, executor)) : this);
});
$p.nX = (function(func, executor) {
  $p_s_concurrent_impl_Promise$DefaultPromise__dispatchOrAddCallbacks__O__s_concurrent_impl_Promise$Callbacks__s_concurrent_impl_Promise$Callbacks(this, this.L, $ct_s_concurrent_impl_Promise$Transformation__I__F1__s_concurrent_ExecutionContext__(new $c_s_concurrent_impl_Promise$Transformation(), 6, func, executor));
});
$p.t = (function() {
  var \u03b4this$tailLocal1 = this;
  while (true) {
    var state = \u03b4this$tailLocal1.L;
    if ((state instanceof $c_s_util_Try)) {
      return (("Future(" + state) + ")");
    } else if ((state instanceof $c_s_concurrent_impl_Promise$Link)) {
      \u03b4this$tailLocal1 = state.eV(\u03b4this$tailLocal1);
    } else {
      return "Future(<not completed>)";
    }
  }
});
$p.rB = (function(value) {
  var state = this.L;
  return ((!(state instanceof $c_s_util_Try)) && this.ea(state, $m_s_concurrent_impl_Promise$().gd(value)));
});
$p.ea = (function(state, resolved) {
  var \u03b4this$tailLocal3 = this;
  var state$tailLocal1 = state;
  while (true) {
    if ($is_s_concurrent_impl_Promise$Callbacks(state$tailLocal1)) {
      if ((!\u03b4this$tailLocal3.fY(state$tailLocal1, resolved))) {
        state$tailLocal1 = \u03b4this$tailLocal3.L;
        continue;
      }
      if ((state$tailLocal1 !== $m_s_concurrent_impl_Promise$().fJ)) {
        $p_s_concurrent_impl_Promise$DefaultPromise__submitWithValue__s_concurrent_impl_Promise$Callbacks__s_util_Try__V(\u03b4this$tailLocal3, state$tailLocal1, resolved);
      }
      return true;
    } else if ((state$tailLocal1 instanceof $c_s_concurrent_impl_Promise$Link)) {
      var p = state$tailLocal1.eV(\u03b4this$tailLocal3);
      if ((p !== \u03b4this$tailLocal3)) {
        var state$tailLocal1$tmp1 = p.L;
        \u03b4this$tailLocal3 = p;
        state$tailLocal1 = state$tailLocal1$tmp1;
        continue;
      }
      return false;
    } else {
      return false;
    }
  }
});
$p.iN = (function(other) {
  if ((other !== this)) {
    var state = this.L;
    if ((!(state instanceof $c_s_util_Try))) {
      if ((other instanceof $c_s_concurrent_impl_Promise$DefaultPromise)) {
        var resolved = $p_s_concurrent_impl_Promise$DefaultPromise__value0__s_util_Try(other);
      } else {
        var this$1 = $m_s_Option$().n9($p_s_concurrent_impl_Promise$DefaultPromise__value0__s_util_Try(other));
        var resolved = (this$1.c() ? null : this$1.s());
      }
      if ((resolved !== null)) {
        this.ea(state, resolved);
      } else {
        other.nX(this, $m_s_concurrent_ExecutionContext$parasitic$());
      }
    }
  }
  return this;
});
$p.je = (function(target, link) {
  var \u03b4this$tailLocal5 = this;
  var link$tailLocal1 = link;
  var target$tailLocal2 = target;
  while (true) {
    if ((\u03b4this$tailLocal5 !== target$tailLocal2)) {
      var state = \u03b4this$tailLocal5.L;
      if ((state instanceof $c_s_util_Try)) {
        if ((!target$tailLocal2.ea(target$tailLocal2.L, state))) {
          throw new $c_jl_IllegalStateException("Cannot link completed promises together");
        } else {
          return (void 0);
        }
      } else if ($is_s_concurrent_impl_Promise$Callbacks(state)) {
        var l = ((link$tailLocal1 !== null) ? link$tailLocal1 : new $c_s_concurrent_impl_Promise$Link(target$tailLocal2));
        var p = l.eV(\u03b4this$tailLocal5);
        if (((\u03b4this$tailLocal5 !== p) && \u03b4this$tailLocal5.fY(state, l))) {
          if ((state !== $m_s_concurrent_impl_Promise$().fJ)) {
            $p_s_concurrent_impl_Promise$DefaultPromise__dispatchOrAddCallbacks__O__s_concurrent_impl_Promise$Callbacks__s_concurrent_impl_Promise$Callbacks(p, p.L, state);
            return (void 0);
          } else {
            return (void 0);
          }
        } else {
          target$tailLocal2 = p;
          link$tailLocal1 = l;
        }
      } else {
        \u03b4this$tailLocal5 = state.eV(\u03b4this$tailLocal5);
      }
    } else {
      return (void 0);
    }
  }
});
$p.rD = (function(resolved) {
  var \u03b4this$tailLocal6 = this;
  while (true) {
    var state = \u03b4this$tailLocal6.L;
    if ((state instanceof $c_s_concurrent_impl_Promise$Link)) {
      var next = (\u03b4this$tailLocal6.fY(state, resolved) ? state.L : \u03b4this$tailLocal6);
      \u03b4this$tailLocal6 = next;
    } else {
      \u03b4this$tailLocal6.ea(state, resolved);
      return (void 0);
    }
  }
});
$p.b = (function(v1) {
  this.ea(this.L, v1);
});
function $isArrayOf_s_concurrent_impl_Promise$DefaultPromise(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.aY)));
}
var $d_s_concurrent_impl_Promise$DefaultPromise = new $TypeData().i($c_s_concurrent_impl_Promise$DefaultPromise, "scala.concurrent.impl.Promise$DefaultPromise", ({
  aY: 1,
  aG: 1,
  a: 1,
  ct: 1,
  cq: 1,
  cs: 1,
  e: 1
}));
/** @constructor */
function $c_s_reflect_AnyValManifest() {
  this.Q = null;
}
$p = $c_s_reflect_AnyValManifest.prototype = new $h_O();
$p.constructor = $c_s_reflect_AnyValManifest;
/** @constructor */
function $h_s_reflect_AnyValManifest() {
}
$h_s_reflect_AnyValManifest.prototype = $p;
$p.t = (function() {
  return this.Q;
});
$p.k = (function(that) {
  return (this === that);
});
$p.r = (function() {
  return $systemIdentityHashCode(this);
});
/** @constructor */
function $c_s_reflect_ManifestFactory$ClassTypeManifest() {
}
$p = $c_s_reflect_ManifestFactory$ClassTypeManifest.prototype = new $h_O();
$p.constructor = $c_s_reflect_ManifestFactory$ClassTypeManifest;
/** @constructor */
function $h_s_reflect_ManifestFactory$ClassTypeManifest() {
}
$h_s_reflect_ManifestFactory$ClassTypeManifest.prototype = $p;
class $c_sjs_js_JavaScriptException extends $c_jl_RuntimeException {
  constructor(exception) {
    super();
    this.K = null;
    this.K = exception;
    $ct_jl_Throwable__T__jl_Throwable__Z__Z__(this, null, null, true, true);
  }
  eS() {
    return $dp_toString__T(this.K);
  }
  aP() {
    return "JavaScriptException";
  }
  aN() {
    return 1;
  }
  aO(x$1) {
    return ((x$1 === 0) ? this.K : $m_sr_Statics$().qr(x$1));
  }
  bx() {
    return new $c_sr_ScalaRunTime$$anon$1(this);
  }
  r() {
    return $m_s_util_hashing_MurmurHash3$().e7(this, 1744042595, true);
  }
  k(x$1) {
    return ((this === x$1) || ((x$1 instanceof $c_sjs_js_JavaScriptException) && $m_sr_BoxesRunTime$().j(this.K, x$1.K)));
  }
}
function $isArrayOf_sjs_js_JavaScriptException(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.cA)));
}
var $d_sjs_js_JavaScriptException = new $TypeData().i($c_sjs_js_JavaScriptException, "scala.scalajs.js.JavaScriptException", ({
  cA: 1,
  D: 1,
  B: 1,
  s: 1,
  a: 1,
  E: 1,
  d: 1
}));
function $f_Lcom_raquo_airstream_core_WritableSignal__setCurrentValue__s_util_Try__V($thiz, newValue) {
  if ((!($thiz.jh() === (void 0)))) {
    $thiz.iE($m_Lcom_raquo_airstream_core_Signal$().nS());
  }
  $thiz.nQ(newValue);
}
function $f_Lcom_raquo_airstream_core_WritableSignal__tryNow__s_util_Try($thiz) {
  var x = $thiz.jh();
  if ((x === (void 0))) {
    $thiz.iE($m_Lcom_raquo_airstream_core_Signal$().nS());
    var nextValue = $thiz.iQ();
    $f_Lcom_raquo_airstream_core_WritableSignal__setCurrentValue__s_util_Try__V($thiz, nextValue);
    var $x_1 = nextValue;
  } else {
    var $x_1 = x;
  }
  return $x_1;
}
function $f_Lcom_raquo_airstream_core_WritableSignal__fireValue__O__Lcom_raquo_airstream_core_Transaction__V($thiz, nextValue, transaction) {
  $f_Lcom_raquo_airstream_core_WritableSignal__fireTry__s_util_Try__Lcom_raquo_airstream_core_Transaction__V($thiz, new $c_s_util_Success(nextValue), transaction);
}
function $f_Lcom_raquo_airstream_core_WritableSignal__fireError__jl_Throwable__Lcom_raquo_airstream_core_Transaction__V($thiz, nextError, transaction) {
  $f_Lcom_raquo_airstream_core_WritableSignal__fireTry__s_util_Try__Lcom_raquo_airstream_core_Transaction__V($thiz, new $c_s_util_Failure(nextError), transaction);
}
function $f_Lcom_raquo_airstream_core_WritableSignal__fireTry__s_util_Try__Lcom_raquo_airstream_core_Transaction__V($thiz, nextValue, transaction) {
  $f_Lcom_raquo_airstream_core_WritableSignal__setCurrentValue__s_util_Try__V($thiz, nextValue);
  var isError = nextValue.nH();
  var elem = false;
  elem = false;
  $thiz.cu(false);
  var this$ = $thiz.cV();
  var index = 0;
  while ((index < (this$.length | 0))) {
    var observer = this$[index];
    index = ((1 + index) | 0);
    observer.e5(nextValue);
    if ((isError && (!elem))) {
      var ev$5 = true;
      elem = ev$5;
    }
  }
  var this$$1 = $thiz.cX();
  var index$1 = 0;
  while ((index$1 < (this$$1.length | 0))) {
    var observer$1 = this$$1[index$1];
    index$1 = ((1 + index$1) | 0);
    observer$1.hh(nextValue, transaction);
    if ((isError && (!elem))) {
      var ev$6 = true;
      elem = ev$6;
    }
  }
  $thiz.cu(true);
  var x = $thiz.e4();
  if ((x !== (void 0))) {
    var i = 0;
    var len = (x.length | 0);
    while ((i < len)) {
      x[i].F();
      i = ((1 + i) | 0);
    }
    x.length = 0;
  }
  if ((isError && (!elem))) {
    nextValue.c8(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((err) => {
      $m_Lcom_raquo_airstream_core_AirstreamError$().c2(err);
    })), new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((_$1) => (void 0))));
  }
}
function $f_Lcom_raquo_airstream_core_WritableStream__fireValue__O__Lcom_raquo_airstream_core_Transaction__V($thiz, nextValue, transaction) {
  $thiz.cu(false);
  var this$ = $thiz.cV();
  var index = 0;
  while ((index < (this$.length | 0))) {
    var observer = this$[index];
    index = ((1 + index) | 0);
    try {
      observer.jm(nextValue);
    } catch (e) {
      var e$2 = ((e instanceof $c_jl_Throwable) ? e : new $c_sjs_js_JavaScriptException(e));
      $m_Lcom_raquo_airstream_core_AirstreamError$().c2(new $c_Lcom_raquo_airstream_core_AirstreamError$ObserverError(e$2));
    }
  }
  var this$$1 = $thiz.cX();
  var index$1 = 0;
  while ((index$1 < (this$$1.length | 0))) {
    var observer$1 = this$$1[index$1];
    index$1 = ((1 + index$1) | 0);
    observer$1.jl(nextValue, transaction);
  }
  $thiz.cu(true);
  var x = $thiz.e4();
  if ((x !== (void 0))) {
    var i = 0;
    var len = (x.length | 0);
    while ((i < len)) {
      x[i].F();
      i = ((1 + i) | 0);
    }
    x.length = 0;
  }
}
function $f_Lcom_raquo_airstream_core_WritableStream__fireError__jl_Throwable__Lcom_raquo_airstream_core_Transaction__V($thiz, nextError, transaction) {
  $thiz.cu(false);
  var this$ = $thiz.cV();
  var index = 0;
  while ((index < (this$.length | 0))) {
    var observer = this$[index];
    index = ((1 + index) | 0);
    observer.g9(nextError);
  }
  var this$$1 = $thiz.cX();
  var index$1 = 0;
  while ((index$1 < (this$$1.length | 0))) {
    var observer$1 = this$$1[index$1];
    index$1 = ((1 + index$1) | 0);
    observer$1.nZ(nextError, transaction);
  }
  $thiz.cu(true);
  var x = $thiz.e4();
  if ((x !== (void 0))) {
    var i = 0;
    var len = (x.length | 0);
    while ((i < len)) {
      x[i].F();
      i = ((1 + i) | 0);
    }
    x.length = 0;
  }
}
function $p_jl_JSConsoleBasedPrintStream__doWriteLine__T__V($thiz, line) {
  if (((typeof console) !== "undefined")) {
    if (($thiz.lO && (!(!(!(!console.error)))))) {
      console.error(line);
    } else {
      console.log(line);
    }
  }
}
/** @constructor */
function $c_jl_JSConsoleBasedPrintStream(isErr) {
  this.lO = false;
  this.fm = null;
  this.lO = isErr;
  $ct_Ljava_io_PrintStream__Ljava_io_OutputStream__Z__Ljava_nio_charset_Charset__(this, new $c_jl_JSConsoleBasedPrintStream$DummyOutputStream(), false, null);
  this.fm = "";
}
$p = $c_jl_JSConsoleBasedPrintStream.prototype = new $h_Ljava_io_PrintStream();
$p.constructor = $c_jl_JSConsoleBasedPrintStream;
/** @constructor */
function $h_jl_JSConsoleBasedPrintStream() {
}
$h_jl_JSConsoleBasedPrintStream.prototype = $p;
$p.qP = (function(s) {
  this.nK(((s === null) ? "null" : s));
});
$p.nK = (function(s) {
  var rest = s;
  while ((rest !== "")) {
    var this$1 = rest;
    var nlPos = (this$1.indexOf("\n") | 0);
    if ((nlPos < 0)) {
      this.fm = (("" + this.fm) + rest);
      rest = "";
    } else {
      var $x_1 = this.fm;
      var this$2 = rest;
      $p_jl_JSConsoleBasedPrintStream__doWriteLine__T__V(this, (("" + $x_1) + this$2.substring(0, nlPos)));
      this.fm = "";
      var this$4 = rest;
      var beginIndex = ((1 + nlPos) | 0);
      rest = this$4.substring(beginIndex);
    }
  }
});
var $d_jl_JSConsoleBasedPrintStream = new $TypeData().i($c_jl_JSConsoleBasedPrintStream, "java.lang.JSConsoleBasedPrintStream", ({
  eH: 1,
  eu: 1,
  et: 1,
  br: 1,
  bp: 1,
  bt: 1,
  bq: 1,
  bs: 1
}));
function $p_sc_StrictOptimizedLinearSeqOps__loop$2__I__sc_LinearSeq__sc_LinearSeq($thiz, n, s) {
  var s$tailLocal1 = s;
  var n$tailLocal1 = n;
  while (true) {
    if (((n$tailLocal1 <= 0) || s$tailLocal1.c())) {
      return s$tailLocal1;
    } else {
      var n$tailLocal1$tmp1 = ((n$tailLocal1 - 1) | 0);
      var s$tailLocal1$tmp1 = s$tailLocal1.l();
      n$tailLocal1 = n$tailLocal1$tmp1;
      s$tailLocal1 = s$tailLocal1$tmp1;
    }
  }
}
function $f_sci_StrictOptimizedSeqOps__distinctBy__F1__O($thiz, f) {
  if (($thiz.bc(1) <= 0)) {
    return $thiz;
  } else {
    var builder = $thiz.g8();
    var seen = $ct_scm_HashSet__(new $c_scm_HashSet());
    var it = $thiz.i();
    var different = false;
    while (it.m()) {
      var next = it.g();
      if (seen.gV(f.b(next))) {
        builder.aV(next);
      } else {
        different = true;
      }
    }
    return (different ? builder.b2() : $thiz);
  }
}
/** @constructor */
function $c_s_reflect_ManifestFactory$BooleanManifest() {
  this.Q = null;
}
$p = $c_s_reflect_ManifestFactory$BooleanManifest.prototype = new $h_s_reflect_AnyValManifest();
$p.constructor = $c_s_reflect_ManifestFactory$BooleanManifest;
/** @constructor */
function $h_s_reflect_ManifestFactory$BooleanManifest() {
}
$h_s_reflect_ManifestFactory$BooleanManifest.prototype = $p;
$p.aC = (function() {
  return $d_Z.l();
});
$p.bo = (function(len) {
  return new $ac_Z(len);
});
/** @constructor */
function $c_s_reflect_ManifestFactory$ByteManifest() {
  this.Q = null;
}
$p = $c_s_reflect_ManifestFactory$ByteManifest.prototype = new $h_s_reflect_AnyValManifest();
$p.constructor = $c_s_reflect_ManifestFactory$ByteManifest;
/** @constructor */
function $h_s_reflect_ManifestFactory$ByteManifest() {
}
$h_s_reflect_ManifestFactory$ByteManifest.prototype = $p;
$p.aC = (function() {
  return $d_B.l();
});
$p.bo = (function(len) {
  return new $ac_B(len);
});
/** @constructor */
function $c_s_reflect_ManifestFactory$CharManifest() {
  this.Q = null;
}
$p = $c_s_reflect_ManifestFactory$CharManifest.prototype = new $h_s_reflect_AnyValManifest();
$p.constructor = $c_s_reflect_ManifestFactory$CharManifest;
/** @constructor */
function $h_s_reflect_ManifestFactory$CharManifest() {
}
$h_s_reflect_ManifestFactory$CharManifest.prototype = $p;
$p.aC = (function() {
  return $d_C.l();
});
$p.bo = (function(len) {
  return new $ac_C(len);
});
/** @constructor */
function $c_s_reflect_ManifestFactory$DoubleManifest() {
  this.Q = null;
}
$p = $c_s_reflect_ManifestFactory$DoubleManifest.prototype = new $h_s_reflect_AnyValManifest();
$p.constructor = $c_s_reflect_ManifestFactory$DoubleManifest;
/** @constructor */
function $h_s_reflect_ManifestFactory$DoubleManifest() {
}
$h_s_reflect_ManifestFactory$DoubleManifest.prototype = $p;
$p.aC = (function() {
  return $d_D.l();
});
$p.bo = (function(len) {
  return new $ac_D(len);
});
/** @constructor */
function $c_s_reflect_ManifestFactory$FloatManifest() {
  this.Q = null;
}
$p = $c_s_reflect_ManifestFactory$FloatManifest.prototype = new $h_s_reflect_AnyValManifest();
$p.constructor = $c_s_reflect_ManifestFactory$FloatManifest;
/** @constructor */
function $h_s_reflect_ManifestFactory$FloatManifest() {
}
$h_s_reflect_ManifestFactory$FloatManifest.prototype = $p;
$p.aC = (function() {
  return $d_F.l();
});
$p.bo = (function(len) {
  return new $ac_F(len);
});
/** @constructor */
function $c_s_reflect_ManifestFactory$IntManifest() {
  this.Q = null;
}
$p = $c_s_reflect_ManifestFactory$IntManifest.prototype = new $h_s_reflect_AnyValManifest();
$p.constructor = $c_s_reflect_ManifestFactory$IntManifest;
/** @constructor */
function $h_s_reflect_ManifestFactory$IntManifest() {
}
$h_s_reflect_ManifestFactory$IntManifest.prototype = $p;
$p.aC = (function() {
  return $d_I.l();
});
$p.bo = (function(len) {
  return new $ac_I(len);
});
/** @constructor */
function $c_s_reflect_ManifestFactory$LongManifest() {
  this.Q = null;
}
$p = $c_s_reflect_ManifestFactory$LongManifest.prototype = new $h_s_reflect_AnyValManifest();
$p.constructor = $c_s_reflect_ManifestFactory$LongManifest;
/** @constructor */
function $h_s_reflect_ManifestFactory$LongManifest() {
}
$h_s_reflect_ManifestFactory$LongManifest.prototype = $p;
$p.aC = (function() {
  return $d_J.l();
});
$p.bo = (function(len) {
  return new $ac_J(len);
});
/** @constructor */
function $c_s_reflect_ManifestFactory$PhantomManifest() {
  this.cS = null;
}
$p = $c_s_reflect_ManifestFactory$PhantomManifest.prototype = new $h_s_reflect_ManifestFactory$ClassTypeManifest();
$p.constructor = $c_s_reflect_ManifestFactory$PhantomManifest;
/** @constructor */
function $h_s_reflect_ManifestFactory$PhantomManifest() {
}
$h_s_reflect_ManifestFactory$PhantomManifest.prototype = $p;
$p.t = (function() {
  return this.cS;
});
$p.k = (function(that) {
  return (this === that);
});
$p.r = (function() {
  return $systemIdentityHashCode(this);
});
/** @constructor */
function $c_s_reflect_ManifestFactory$ShortManifest() {
  this.Q = null;
}
$p = $c_s_reflect_ManifestFactory$ShortManifest.prototype = new $h_s_reflect_AnyValManifest();
$p.constructor = $c_s_reflect_ManifestFactory$ShortManifest;
/** @constructor */
function $h_s_reflect_ManifestFactory$ShortManifest() {
}
$h_s_reflect_ManifestFactory$ShortManifest.prototype = $p;
$p.aC = (function() {
  return $d_S.l();
});
$p.bo = (function(len) {
  return new $ac_S(len);
});
/** @constructor */
function $c_s_reflect_ManifestFactory$UnitManifest() {
  this.Q = null;
}
$p = $c_s_reflect_ManifestFactory$UnitManifest.prototype = new $h_s_reflect_AnyValManifest();
$p.constructor = $c_s_reflect_ManifestFactory$UnitManifest;
/** @constructor */
function $h_s_reflect_ManifestFactory$UnitManifest() {
}
$h_s_reflect_ManifestFactory$UnitManifest.prototype = $p;
$p.aC = (function() {
  return $d_V.l();
});
$p.bo = (function(len) {
  return new ($d_jl_Void.r().C)(len);
});
/** @constructor */
function $c_sc_AbstractView() {
}
$p = $c_sc_AbstractView.prototype = new $h_sc_AbstractIterable();
$p.constructor = $c_sc_AbstractView;
/** @constructor */
function $h_sc_AbstractView() {
}
$h_sc_AbstractView.prototype = $p;
$p.bn = (function() {
  return $m_sc_View$();
});
$p.t = (function() {
  return $f_sc_View__toString__T(this);
});
$p.bq = (function() {
  return "View";
});
function $f_sc_Set__equals__O__Z($thiz, that) {
  if (($thiz === that)) {
    return true;
  } else if ($is_sc_Set(that)) {
    if (($thiz.ax() === that.ax())) {
      try {
        return $thiz.ri(that);
      } catch (e) {
        if (false) {
          return false;
        } else {
          throw e;
        }
      }
    } else {
      return false;
    }
  } else {
    return false;
  }
}
function $is_sc_Set(obj) {
  return (!(!((obj && obj.$classData) && obj.$classData.n.aN)));
}
function $isArrayOf_sc_Set(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.aN)));
}
/** @constructor */
function $c_s_reflect_ManifestFactory$AnyManifest$() {
  this.cS = null;
  this.cS = "Any";
  $m_sci_Nil$();
}
$p = $c_s_reflect_ManifestFactory$AnyManifest$.prototype = new $h_s_reflect_ManifestFactory$PhantomManifest();
$p.constructor = $c_s_reflect_ManifestFactory$AnyManifest$;
/** @constructor */
function $h_s_reflect_ManifestFactory$AnyManifest$() {
}
$h_s_reflect_ManifestFactory$AnyManifest$.prototype = $p;
$p.aC = (function() {
  return $d_O.l();
});
$p.bo = (function(len) {
  return new $ac_O(len);
});
var $d_s_reflect_ManifestFactory$AnyManifest$ = new $TypeData().i($c_s_reflect_ManifestFactory$AnyManifest$, "scala.reflect.ManifestFactory$AnyManifest$", ({
  hj: 1,
  ax: 1,
  aw: 1,
  a: 1,
  Q: 1,
  P: 1,
  d: 1,
  F: 1,
  T: 1
}));
var $n_s_reflect_ManifestFactory$AnyManifest$;
function $m_s_reflect_ManifestFactory$AnyManifest$() {
  if ((!$n_s_reflect_ManifestFactory$AnyManifest$)) {
    $n_s_reflect_ManifestFactory$AnyManifest$ = new $c_s_reflect_ManifestFactory$AnyManifest$();
  }
  return $n_s_reflect_ManifestFactory$AnyManifest$;
}
/** @constructor */
function $c_s_reflect_ManifestFactory$BooleanManifest$() {
  this.Q = null;
  this.Q = "Boolean";
}
$p = $c_s_reflect_ManifestFactory$BooleanManifest$.prototype = new $h_s_reflect_ManifestFactory$BooleanManifest();
$p.constructor = $c_s_reflect_ManifestFactory$BooleanManifest$;
/** @constructor */
function $h_s_reflect_ManifestFactory$BooleanManifest$() {
}
$h_s_reflect_ManifestFactory$BooleanManifest$.prototype = $p;
var $d_s_reflect_ManifestFactory$BooleanManifest$ = new $TypeData().i($c_s_reflect_ManifestFactory$BooleanManifest$, "scala.reflect.ManifestFactory$BooleanManifest$", ({
  hl: 1,
  hk: 1,
  a4: 1,
  a: 1,
  Q: 1,
  P: 1,
  d: 1,
  F: 1,
  T: 1
}));
var $n_s_reflect_ManifestFactory$BooleanManifest$;
function $m_s_reflect_ManifestFactory$BooleanManifest$() {
  if ((!$n_s_reflect_ManifestFactory$BooleanManifest$)) {
    $n_s_reflect_ManifestFactory$BooleanManifest$ = new $c_s_reflect_ManifestFactory$BooleanManifest$();
  }
  return $n_s_reflect_ManifestFactory$BooleanManifest$;
}
/** @constructor */
function $c_s_reflect_ManifestFactory$ByteManifest$() {
  this.Q = null;
  this.Q = "Byte";
}
$p = $c_s_reflect_ManifestFactory$ByteManifest$.prototype = new $h_s_reflect_ManifestFactory$ByteManifest();
$p.constructor = $c_s_reflect_ManifestFactory$ByteManifest$;
/** @constructor */
function $h_s_reflect_ManifestFactory$ByteManifest$() {
}
$h_s_reflect_ManifestFactory$ByteManifest$.prototype = $p;
var $d_s_reflect_ManifestFactory$ByteManifest$ = new $TypeData().i($c_s_reflect_ManifestFactory$ByteManifest$, "scala.reflect.ManifestFactory$ByteManifest$", ({
  hn: 1,
  hm: 1,
  a4: 1,
  a: 1,
  Q: 1,
  P: 1,
  d: 1,
  F: 1,
  T: 1
}));
var $n_s_reflect_ManifestFactory$ByteManifest$;
function $m_s_reflect_ManifestFactory$ByteManifest$() {
  if ((!$n_s_reflect_ManifestFactory$ByteManifest$)) {
    $n_s_reflect_ManifestFactory$ByteManifest$ = new $c_s_reflect_ManifestFactory$ByteManifest$();
  }
  return $n_s_reflect_ManifestFactory$ByteManifest$;
}
/** @constructor */
function $c_s_reflect_ManifestFactory$CharManifest$() {
  this.Q = null;
  this.Q = "Char";
}
$p = $c_s_reflect_ManifestFactory$CharManifest$.prototype = new $h_s_reflect_ManifestFactory$CharManifest();
$p.constructor = $c_s_reflect_ManifestFactory$CharManifest$;
/** @constructor */
function $h_s_reflect_ManifestFactory$CharManifest$() {
}
$h_s_reflect_ManifestFactory$CharManifest$.prototype = $p;
var $d_s_reflect_ManifestFactory$CharManifest$ = new $TypeData().i($c_s_reflect_ManifestFactory$CharManifest$, "scala.reflect.ManifestFactory$CharManifest$", ({
  hp: 1,
  ho: 1,
  a4: 1,
  a: 1,
  Q: 1,
  P: 1,
  d: 1,
  F: 1,
  T: 1
}));
var $n_s_reflect_ManifestFactory$CharManifest$;
function $m_s_reflect_ManifestFactory$CharManifest$() {
  if ((!$n_s_reflect_ManifestFactory$CharManifest$)) {
    $n_s_reflect_ManifestFactory$CharManifest$ = new $c_s_reflect_ManifestFactory$CharManifest$();
  }
  return $n_s_reflect_ManifestFactory$CharManifest$;
}
/** @constructor */
function $c_s_reflect_ManifestFactory$DoubleManifest$() {
  this.Q = null;
  this.Q = "Double";
}
$p = $c_s_reflect_ManifestFactory$DoubleManifest$.prototype = new $h_s_reflect_ManifestFactory$DoubleManifest();
$p.constructor = $c_s_reflect_ManifestFactory$DoubleManifest$;
/** @constructor */
function $h_s_reflect_ManifestFactory$DoubleManifest$() {
}
$h_s_reflect_ManifestFactory$DoubleManifest$.prototype = $p;
var $d_s_reflect_ManifestFactory$DoubleManifest$ = new $TypeData().i($c_s_reflect_ManifestFactory$DoubleManifest$, "scala.reflect.ManifestFactory$DoubleManifest$", ({
  hr: 1,
  hq: 1,
  a4: 1,
  a: 1,
  Q: 1,
  P: 1,
  d: 1,
  F: 1,
  T: 1
}));
var $n_s_reflect_ManifestFactory$DoubleManifest$;
function $m_s_reflect_ManifestFactory$DoubleManifest$() {
  if ((!$n_s_reflect_ManifestFactory$DoubleManifest$)) {
    $n_s_reflect_ManifestFactory$DoubleManifest$ = new $c_s_reflect_ManifestFactory$DoubleManifest$();
  }
  return $n_s_reflect_ManifestFactory$DoubleManifest$;
}
/** @constructor */
function $c_s_reflect_ManifestFactory$FloatManifest$() {
  this.Q = null;
  this.Q = "Float";
}
$p = $c_s_reflect_ManifestFactory$FloatManifest$.prototype = new $h_s_reflect_ManifestFactory$FloatManifest();
$p.constructor = $c_s_reflect_ManifestFactory$FloatManifest$;
/** @constructor */
function $h_s_reflect_ManifestFactory$FloatManifest$() {
}
$h_s_reflect_ManifestFactory$FloatManifest$.prototype = $p;
var $d_s_reflect_ManifestFactory$FloatManifest$ = new $TypeData().i($c_s_reflect_ManifestFactory$FloatManifest$, "scala.reflect.ManifestFactory$FloatManifest$", ({
  ht: 1,
  hs: 1,
  a4: 1,
  a: 1,
  Q: 1,
  P: 1,
  d: 1,
  F: 1,
  T: 1
}));
var $n_s_reflect_ManifestFactory$FloatManifest$;
function $m_s_reflect_ManifestFactory$FloatManifest$() {
  if ((!$n_s_reflect_ManifestFactory$FloatManifest$)) {
    $n_s_reflect_ManifestFactory$FloatManifest$ = new $c_s_reflect_ManifestFactory$FloatManifest$();
  }
  return $n_s_reflect_ManifestFactory$FloatManifest$;
}
/** @constructor */
function $c_s_reflect_ManifestFactory$IntManifest$() {
  this.Q = null;
  this.Q = "Int";
}
$p = $c_s_reflect_ManifestFactory$IntManifest$.prototype = new $h_s_reflect_ManifestFactory$IntManifest();
$p.constructor = $c_s_reflect_ManifestFactory$IntManifest$;
/** @constructor */
function $h_s_reflect_ManifestFactory$IntManifest$() {
}
$h_s_reflect_ManifestFactory$IntManifest$.prototype = $p;
var $d_s_reflect_ManifestFactory$IntManifest$ = new $TypeData().i($c_s_reflect_ManifestFactory$IntManifest$, "scala.reflect.ManifestFactory$IntManifest$", ({
  hv: 1,
  hu: 1,
  a4: 1,
  a: 1,
  Q: 1,
  P: 1,
  d: 1,
  F: 1,
  T: 1
}));
var $n_s_reflect_ManifestFactory$IntManifest$;
function $m_s_reflect_ManifestFactory$IntManifest$() {
  if ((!$n_s_reflect_ManifestFactory$IntManifest$)) {
    $n_s_reflect_ManifestFactory$IntManifest$ = new $c_s_reflect_ManifestFactory$IntManifest$();
  }
  return $n_s_reflect_ManifestFactory$IntManifest$;
}
/** @constructor */
function $c_s_reflect_ManifestFactory$LongManifest$() {
  this.Q = null;
  this.Q = "Long";
}
$p = $c_s_reflect_ManifestFactory$LongManifest$.prototype = new $h_s_reflect_ManifestFactory$LongManifest();
$p.constructor = $c_s_reflect_ManifestFactory$LongManifest$;
/** @constructor */
function $h_s_reflect_ManifestFactory$LongManifest$() {
}
$h_s_reflect_ManifestFactory$LongManifest$.prototype = $p;
var $d_s_reflect_ManifestFactory$LongManifest$ = new $TypeData().i($c_s_reflect_ManifestFactory$LongManifest$, "scala.reflect.ManifestFactory$LongManifest$", ({
  hx: 1,
  hw: 1,
  a4: 1,
  a: 1,
  Q: 1,
  P: 1,
  d: 1,
  F: 1,
  T: 1
}));
var $n_s_reflect_ManifestFactory$LongManifest$;
function $m_s_reflect_ManifestFactory$LongManifest$() {
  if ((!$n_s_reflect_ManifestFactory$LongManifest$)) {
    $n_s_reflect_ManifestFactory$LongManifest$ = new $c_s_reflect_ManifestFactory$LongManifest$();
  }
  return $n_s_reflect_ManifestFactory$LongManifest$;
}
/** @constructor */
function $c_s_reflect_ManifestFactory$NothingManifest$() {
  this.cS = null;
  this.cS = "Nothing";
  $m_sci_Nil$();
}
$p = $c_s_reflect_ManifestFactory$NothingManifest$.prototype = new $h_s_reflect_ManifestFactory$PhantomManifest();
$p.constructor = $c_s_reflect_ManifestFactory$NothingManifest$;
/** @constructor */
function $h_s_reflect_ManifestFactory$NothingManifest$() {
}
$h_s_reflect_ManifestFactory$NothingManifest$.prototype = $p;
$p.aC = (function() {
  return $d_sr_Nothing$.l();
});
$p.bo = (function(len) {
  return new ($d_sr_Nothing$.r().C)(len);
});
var $d_s_reflect_ManifestFactory$NothingManifest$ = new $TypeData().i($c_s_reflect_ManifestFactory$NothingManifest$, "scala.reflect.ManifestFactory$NothingManifest$", ({
  hy: 1,
  ax: 1,
  aw: 1,
  a: 1,
  Q: 1,
  P: 1,
  d: 1,
  F: 1,
  T: 1
}));
var $n_s_reflect_ManifestFactory$NothingManifest$;
function $m_s_reflect_ManifestFactory$NothingManifest$() {
  if ((!$n_s_reflect_ManifestFactory$NothingManifest$)) {
    $n_s_reflect_ManifestFactory$NothingManifest$ = new $c_s_reflect_ManifestFactory$NothingManifest$();
  }
  return $n_s_reflect_ManifestFactory$NothingManifest$;
}
/** @constructor */
function $c_s_reflect_ManifestFactory$NullManifest$() {
  this.cS = null;
  this.cS = "Null";
  $m_sci_Nil$();
}
$p = $c_s_reflect_ManifestFactory$NullManifest$.prototype = new $h_s_reflect_ManifestFactory$PhantomManifest();
$p.constructor = $c_s_reflect_ManifestFactory$NullManifest$;
/** @constructor */
function $h_s_reflect_ManifestFactory$NullManifest$() {
}
$h_s_reflect_ManifestFactory$NullManifest$.prototype = $p;
$p.aC = (function() {
  return $d_sr_Null$.l();
});
$p.bo = (function(len) {
  return new ($d_sr_Null$.r().C)(len);
});
var $d_s_reflect_ManifestFactory$NullManifest$ = new $TypeData().i($c_s_reflect_ManifestFactory$NullManifest$, "scala.reflect.ManifestFactory$NullManifest$", ({
  hz: 1,
  ax: 1,
  aw: 1,
  a: 1,
  Q: 1,
  P: 1,
  d: 1,
  F: 1,
  T: 1
}));
var $n_s_reflect_ManifestFactory$NullManifest$;
function $m_s_reflect_ManifestFactory$NullManifest$() {
  if ((!$n_s_reflect_ManifestFactory$NullManifest$)) {
    $n_s_reflect_ManifestFactory$NullManifest$ = new $c_s_reflect_ManifestFactory$NullManifest$();
  }
  return $n_s_reflect_ManifestFactory$NullManifest$;
}
/** @constructor */
function $c_s_reflect_ManifestFactory$ObjectManifest$() {
  this.cS = null;
  this.cS = "Object";
  $m_sci_Nil$();
}
$p = $c_s_reflect_ManifestFactory$ObjectManifest$.prototype = new $h_s_reflect_ManifestFactory$PhantomManifest();
$p.constructor = $c_s_reflect_ManifestFactory$ObjectManifest$;
/** @constructor */
function $h_s_reflect_ManifestFactory$ObjectManifest$() {
}
$h_s_reflect_ManifestFactory$ObjectManifest$.prototype = $p;
$p.aC = (function() {
  return $d_O.l();
});
$p.bo = (function(len) {
  return new $ac_O(len);
});
var $d_s_reflect_ManifestFactory$ObjectManifest$ = new $TypeData().i($c_s_reflect_ManifestFactory$ObjectManifest$, "scala.reflect.ManifestFactory$ObjectManifest$", ({
  hA: 1,
  ax: 1,
  aw: 1,
  a: 1,
  Q: 1,
  P: 1,
  d: 1,
  F: 1,
  T: 1
}));
var $n_s_reflect_ManifestFactory$ObjectManifest$;
function $m_s_reflect_ManifestFactory$ObjectManifest$() {
  if ((!$n_s_reflect_ManifestFactory$ObjectManifest$)) {
    $n_s_reflect_ManifestFactory$ObjectManifest$ = new $c_s_reflect_ManifestFactory$ObjectManifest$();
  }
  return $n_s_reflect_ManifestFactory$ObjectManifest$;
}
/** @constructor */
function $c_s_reflect_ManifestFactory$ShortManifest$() {
  this.Q = null;
  this.Q = "Short";
}
$p = $c_s_reflect_ManifestFactory$ShortManifest$.prototype = new $h_s_reflect_ManifestFactory$ShortManifest();
$p.constructor = $c_s_reflect_ManifestFactory$ShortManifest$;
/** @constructor */
function $h_s_reflect_ManifestFactory$ShortManifest$() {
}
$h_s_reflect_ManifestFactory$ShortManifest$.prototype = $p;
var $d_s_reflect_ManifestFactory$ShortManifest$ = new $TypeData().i($c_s_reflect_ManifestFactory$ShortManifest$, "scala.reflect.ManifestFactory$ShortManifest$", ({
  hC: 1,
  hB: 1,
  a4: 1,
  a: 1,
  Q: 1,
  P: 1,
  d: 1,
  F: 1,
  T: 1
}));
var $n_s_reflect_ManifestFactory$ShortManifest$;
function $m_s_reflect_ManifestFactory$ShortManifest$() {
  if ((!$n_s_reflect_ManifestFactory$ShortManifest$)) {
    $n_s_reflect_ManifestFactory$ShortManifest$ = new $c_s_reflect_ManifestFactory$ShortManifest$();
  }
  return $n_s_reflect_ManifestFactory$ShortManifest$;
}
/** @constructor */
function $c_s_reflect_ManifestFactory$UnitManifest$() {
  this.Q = null;
  this.Q = "Unit";
}
$p = $c_s_reflect_ManifestFactory$UnitManifest$.prototype = new $h_s_reflect_ManifestFactory$UnitManifest();
$p.constructor = $c_s_reflect_ManifestFactory$UnitManifest$;
/** @constructor */
function $h_s_reflect_ManifestFactory$UnitManifest$() {
}
$h_s_reflect_ManifestFactory$UnitManifest$.prototype = $p;
var $d_s_reflect_ManifestFactory$UnitManifest$ = new $TypeData().i($c_s_reflect_ManifestFactory$UnitManifest$, "scala.reflect.ManifestFactory$UnitManifest$", ({
  hE: 1,
  hD: 1,
  a4: 1,
  a: 1,
  Q: 1,
  P: 1,
  d: 1,
  F: 1,
  T: 1
}));
var $n_s_reflect_ManifestFactory$UnitManifest$;
function $m_s_reflect_ManifestFactory$UnitManifest$() {
  if ((!$n_s_reflect_ManifestFactory$UnitManifest$)) {
    $n_s_reflect_ManifestFactory$UnitManifest$ = new $c_s_reflect_ManifestFactory$UnitManifest$();
  }
  return $n_s_reflect_ManifestFactory$UnitManifest$;
}
function $f_Lcom_raquo_airstream_common_SingleParentStream__onStart__V($thiz) {
  $f_Lcom_raquo_airstream_core_WritableObservable__addInternalObserver__Lcom_raquo_airstream_core_InternalObserver__Z__V($thiz.gq, $thiz, false);
}
function $f_Lcom_raquo_airstream_common_SingleParentStream__onStop__V($thiz) {
  $f_Lcom_raquo_airstream_core_BaseObservable__removeInternalObserver__Lcom_raquo_airstream_core_InternalObserver__V($thiz.gq, $thiz);
}
/** @constructor */
function $c_Lcom_raquo_airstream_custom_CustomStreamSource(makeConfig) {
  this.jM = null;
  this.jL = false;
  this.jN = null;
  this.jJ = null;
  this.jK = null;
  this.jP = false;
  this.jO = 0;
  this.gp = 0;
  this.go = null;
  this.jM = (void 0);
  $f_Lcom_raquo_airstream_core_BaseObservable__$init$__V(this);
  $f_Lcom_raquo_airstream_core_WritableObservable__$init$__V(this);
  $f_Lcom_raquo_airstream_custom_CustomSource__$init$__V(this);
  this.go = makeConfig.pb(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((value) => {
    new $c_Lcom_raquo_airstream_core_Transaction(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((_$1) => {
      $f_Lcom_raquo_airstream_core_WritableStream__fireValue__O__Lcom_raquo_airstream_core_Transaction__V(this, value, _$1);
    })));
  })), new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((err) => {
    new $c_Lcom_raquo_airstream_core_Transaction(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((err$2) => ((_$2) => {
      $f_Lcom_raquo_airstream_core_WritableStream__fireError__jl_Throwable__Lcom_raquo_airstream_core_Transaction__V(this, err$2, _$2);
    }))(err)));
  })), new $c_sjsr_AnonFunction0_$$Lambda$2bf0f8dc580d6edeb2d6a336c52a1bab3049702d((() => this.gp)), new $c_sjsr_AnonFunction0_$$Lambda$2bf0f8dc580d6edeb2d6a336c52a1bab3049702d((() => $f_Lcom_raquo_airstream_core_BaseObservable__isStarted__Z(this))));
}
$p = $c_Lcom_raquo_airstream_custom_CustomStreamSource.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_airstream_custom_CustomStreamSource;
/** @constructor */
function $h_Lcom_raquo_airstream_custom_CustomStreamSource() {
}
$h_Lcom_raquo_airstream_custom_CustomStreamSource.prototype = $p;
$p.e3 = (function() {
  return this.jM;
});
$p.e0 = (function() {
  return $f_Lcom_raquo_airstream_core_Named__defaultDisplayName__T(this);
});
$p.t = (function() {
  return $f_Lcom_raquo_airstream_core_Named__displayName__T(this);
});
$p.g5 = (function() {
  return this.jL;
});
$p.e4 = (function() {
  return this.jN;
});
$p.cu = (function(x$1) {
  this.jL = x$1;
});
$p.g7 = (function(x$1) {
  this.jN = x$1;
});
$p.k = (function(obj) {
  return (this === obj);
});
$p.r = (function() {
  return $systemIdentityHashCode(this);
});
$p.hd = (function(observer) {
});
$p.cV = (function() {
  return this.jJ;
});
$p.cX = (function() {
  return this.jK;
});
$p.ho = (function() {
  return this.jP;
});
$p.f0 = (function(x$1) {
  this.jP = x$1;
});
$p.h1 = (function(x$0) {
  this.jJ = x$0;
});
$p.h2 = (function(x$0) {
  this.jK = x$0;
});
$p.gj = (function() {
  return this.jO;
});
$p.hi = (function() {
  $f_Lcom_raquo_airstream_custom_CustomSource__onWillStart__V(this);
});
$p.hf = (function() {
  $f_Lcom_raquo_airstream_custom_CustomSource__onStart__V(this);
});
$p.hg = (function() {
  $f_Lcom_raquo_airstream_custom_CustomSource__onStop__V(this);
});
$p.gi = (function() {
  return this;
});
var $d_Lcom_raquo_airstream_custom_CustomStreamSource = new $TypeData().i($c_Lcom_raquo_airstream_custom_CustomStreamSource, "com.raquo.airstream.custom.CustomStreamSource", ({
  cW: 1,
  aj: 1,
  a5: 1,
  ao: 1,
  ap: 1,
  b8: 1,
  b6: 1,
  ar: 1,
  ba: 1,
  cS: 1
}));
/** @constructor */
function $c_Lcom_raquo_airstream_state_VarSignal(initial, parentDisplayName) {
  this.kj = null;
  this.ki = false;
  this.kk = null;
  this.hD = 0;
  this.kg = null;
  this.kh = null;
  this.kn = false;
  this.hE = null;
  this.kl = null;
  this.km = 0;
  this.kl = parentDisplayName;
  this.kj = (void 0);
  $f_Lcom_raquo_airstream_core_BaseObservable__$init$__V(this);
  this.hD = 0;
  $f_Lcom_raquo_airstream_core_WritableObservable__$init$__V(this);
  this.hE = (void 0);
  this.km = 1;
  $f_Lcom_raquo_airstream_core_WritableSignal__setCurrentValue__s_util_Try__V(this, initial);
}
$p = $c_Lcom_raquo_airstream_state_VarSignal.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_airstream_state_VarSignal;
/** @constructor */
function $h_Lcom_raquo_airstream_state_VarSignal() {
}
$h_Lcom_raquo_airstream_state_VarSignal.prototype = $p;
$p.e3 = (function() {
  return this.kj;
});
$p.t = (function() {
  return $f_Lcom_raquo_airstream_core_Named__displayName__T(this);
});
$p.g5 = (function() {
  return this.ki;
});
$p.e4 = (function() {
  return this.kk;
});
$p.cu = (function(x$1) {
  this.ki = x$1;
});
$p.g7 = (function(x$1) {
  this.kk = x$1;
});
$p.hg = (function() {
});
$p.k = (function(obj) {
  return (this === obj);
});
$p.r = (function() {
  return $systemIdentityHashCode(this);
});
$p.iD = (function() {
  return this.hD;
});
$p.iE = (function(x$1) {
  this.hD = x$1;
});
$p.hf = (function() {
  $f_Lcom_raquo_airstream_core_Signal__onStart__V(this);
});
$p.hd = (function(observer) {
  observer.e5($f_Lcom_raquo_airstream_core_WritableSignal__tryNow__s_util_Try(this));
});
$p.cV = (function() {
  return this.kg;
});
$p.cX = (function() {
  return this.kh;
});
$p.ho = (function() {
  return this.kn;
});
$p.f0 = (function(x$1) {
  this.kn = x$1;
});
$p.h1 = (function(x$0) {
  this.kg = x$0;
});
$p.h2 = (function(x$0) {
  this.kh = x$0;
});
$p.jh = (function() {
  return this.hE;
});
$p.nQ = (function(x$1) {
  this.hE = x$1;
});
$p.ju = (function() {
  return $f_Lcom_raquo_airstream_core_WritableSignal__tryNow__s_util_Try(this);
});
$p.gj = (function() {
  return this.km;
});
$p.iQ = (function() {
  return $f_Lcom_raquo_airstream_core_WritableSignal__tryNow__s_util_Try(this);
});
$p.hi = (function() {
});
$p.e0 = (function() {
  return (this.kl.F() + ".signal");
});
$p.gi = (function() {
  return this;
});
var $d_Lcom_raquo_airstream_state_VarSignal = new $TypeData().i($c_Lcom_raquo_airstream_state_VarSignal, "com.raquo.airstream.state.VarSignal", ({
  da: 1,
  aj: 1,
  a5: 1,
  ao: 1,
  ap: 1,
  aB: 1,
  b7: 1,
  ar: 1,
  b9: 1,
  d6: 1
}));
function $f_sc_Seq__equals__O__Z($thiz, o) {
  if (($thiz === o)) {
    return true;
  } else {
    if ($is_sc_Seq(o)) {
      if (o.gZ($thiz)) {
        return $thiz.eW(o);
      }
    }
    return false;
  }
}
function $is_sc_Seq(obj) {
  return (!(!((obj && obj.$classData) && obj.$classData.n.m)));
}
function $isArrayOf_sc_Seq(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.m)));
}
/** @constructor */
function $c_sc_View$$anon$1(it$3) {
  this.mb = null;
  this.mb = it$3;
}
$p = $c_sc_View$$anon$1.prototype = new $h_sc_AbstractView();
$p.constructor = $c_sc_View$$anon$1;
/** @constructor */
function $h_sc_View$$anon$1() {
}
$h_sc_View$$anon$1.prototype = $p;
$p.i = (function() {
  return this.mb.F();
});
var $d_sc_View$$anon$1 = new $TypeData().i($c_sc_View$$anon$1, "scala.collection.View$$anon$1", ({
  fH: 1,
  am: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  a: 1,
  ac: 1
}));
/** @constructor */
function $c_sc_View$DistinctBy(underlying, f) {
  this.gH = null;
  this.mc = null;
  this.gH = underlying;
  this.mc = f;
}
$p = $c_sc_View$DistinctBy.prototype = new $h_sc_AbstractView();
$p.constructor = $c_sc_View$DistinctBy;
/** @constructor */
function $h_sc_View$DistinctBy() {
}
$h_sc_View$DistinctBy.prototype = $p;
$p.i = (function() {
  var this$1 = this.gH.i();
  return new $c_sc_Iterator$$anon$8(this.mc, this$1);
});
$p.x = (function() {
  return ((this.gH.x() === 0) ? 0 : (-1));
});
$p.c = (function() {
  return this.gH.c();
});
var $d_sc_View$DistinctBy = new $TypeData().i($c_sc_View$DistinctBy, "scala.collection.View$DistinctBy", ({
  fI: 1,
  am: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  a: 1,
  ac: 1
}));
function $f_Lcom_raquo_airstream_common_SingleParentSignal__$init$__V($thiz) {
  $thiz.hw = ($thiz.cZ !== null);
  $thiz.gr = (-1);
}
function $f_Lcom_raquo_airstream_common_SingleParentSignal__onWillStart__V($thiz) {
  $f_Lcom_raquo_airstream_core_WritableObservable__maybeWillStart__V($thiz.cZ);
  if ($thiz.hw) {
    var newParentLastUpdateId = $thiz.cZ.iD();
    if ((newParentLastUpdateId !== $thiz.gr)) {
      $f_Lcom_raquo_airstream_common_SingleParentSignal__updateCurrentValueFromParent__s_util_Try__I__V($thiz, $thiz.iQ(), newParentLastUpdateId);
    }
  }
}
function $f_Lcom_raquo_airstream_common_SingleParentSignal__updateCurrentValueFromParent__s_util_Try__I__V($thiz, nextValue, nextParentLastUpdateId) {
  $f_Lcom_raquo_airstream_core_WritableSignal__setCurrentValue__s_util_Try__V($thiz, nextValue);
  $thiz.gr = nextParentLastUpdateId;
}
function $f_Lcom_raquo_airstream_common_SingleParentSignal__onTry__s_util_Try__Lcom_raquo_airstream_core_Transaction__V($thiz, nextParentValue, transaction) {
  if ($thiz.hw) {
    $thiz.gr = $thiz.cZ.iD();
  }
}
function $f_Lcom_raquo_airstream_common_SingleParentSignal__onStart__V($thiz) {
  $f_Lcom_raquo_airstream_core_WritableObservable__addInternalObserver__Lcom_raquo_airstream_core_InternalObserver__Z__V($thiz.cZ, $thiz, false);
  $f_Lcom_raquo_airstream_core_Signal__onStart__V($thiz);
}
function $f_Lcom_raquo_airstream_common_SingleParentSignal__onStop__V($thiz) {
  $f_Lcom_raquo_airstream_core_BaseObservable__removeInternalObserver__Lcom_raquo_airstream_core_InternalObserver__V($thiz.cZ, $thiz);
}
/** @constructor */
function $c_sc_AbstractSet() {
}
$p = $c_sc_AbstractSet.prototype = new $h_sc_AbstractIterable();
$p.constructor = $c_sc_AbstractSet;
/** @constructor */
function $h_sc_AbstractSet() {
}
$h_sc_AbstractSet.prototype = $p;
$p.ri = (function(that) {
  return this.eQ(that);
});
$p.k = (function(that) {
  return $f_sc_Set__equals__O__Z(this, that);
});
$p.bq = (function() {
  return "Set";
});
$p.t = (function() {
  return $f_sc_Iterable__toString__T(this);
});
$p.b = (function(v1) {
  return this.bl(v1);
});
function $f_sc_Map__equals__O__Z($thiz, o) {
  if (($thiz === o)) {
    return true;
  } else if ($is_sc_Map(o)) {
    if (($thiz.ax() === o.ax())) {
      try {
        return $thiz.eQ(new $c_sr_AbstractFunction1_$$Lambda$7afc3dd0acc1681fb022ef921c83979087aaa919(((map$1) => ((kv$2) => $m_sr_BoxesRunTime$().j(map$1.c9(kv$2.aZ, new $c_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c((() => $m_sc_Map$().m8.F()))), kv$2.aQ)))(o)));
      } catch (e) {
        if (false) {
          return false;
        } else {
          throw e;
        }
      }
    } else {
      return false;
    }
  } else {
    return false;
  }
}
function $is_sc_Map(obj) {
  return (!(!((obj && obj.$classData) && obj.$classData.n.a2)));
}
function $isArrayOf_sc_Map(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.a2)));
}
function $ct_s_concurrent_impl_Promise$Transformation__F1__s_concurrent_ExecutionContext__s_util_Try__I__($thiz, _fun, _ec, _arg, _xform) {
  $thiz.gO = _fun;
  $thiz.fL = _ec;
  $thiz.fK = _arg;
  $thiz.fM = _xform;
  $ct_s_concurrent_impl_Promise$DefaultPromise__($thiz);
  return $thiz;
}
function $ct_s_concurrent_impl_Promise$Transformation__I__F1__s_concurrent_ExecutionContext__($thiz, xform, f, ec) {
  $ct_s_concurrent_impl_Promise$Transformation__F1__s_concurrent_ExecutionContext__s_util_Try__I__($thiz, f, ec, null, xform);
  return $thiz;
}
function $p_s_concurrent_impl_Promise$Transformation__handleFailure__jl_Throwable__s_concurrent_ExecutionContext__V($thiz, t, e) {
  if ((false || $m_s_util_control_NonFatal$().gW(t))) {
    var completed = $thiz.ea($thiz.L, $m_s_concurrent_impl_Promise$().gd(new $c_s_util_Failure(t)));
    if (((($thiz.fM === 5) || ($thiz.fM === 6)) || (!completed))) {
      e.js(t);
    }
  } else {
    var $x_1 = t;
    throw (($x_1 instanceof $c_sjs_js_JavaScriptException) ? $x_1.K : $x_1);
  }
}
/** @constructor */
function $c_s_concurrent_impl_Promise$Transformation() {
  this.L = null;
  this.gO = null;
  this.fL = null;
  this.fK = null;
  this.fM = 0;
}
$p = $c_s_concurrent_impl_Promise$Transformation.prototype = new $h_s_concurrent_impl_Promise$DefaultPromise();
$p.constructor = $c_s_concurrent_impl_Promise$Transformation;
/** @constructor */
function $h_s_concurrent_impl_Promise$Transformation() {
}
$h_s_concurrent_impl_Promise$Transformation.prototype = $p;
$p.of = (function(resolved) {
  this.fK = resolved;
  var e = this.fL;
  try {
    if ((e === null)) {
      $m_sr_Scala3RunTime$().bp();
    }
    e.iW(this);
  } catch (e$2) {
    var e$3 = ((e$2 instanceof $c_jl_Throwable) ? e$2 : new $c_sjs_js_JavaScriptException(e$2));
    this.gO = null;
    this.fK = null;
    this.fL = null;
    if ((e === null)) {
      $m_sr_Scala3RunTime$().bp();
    }
    $p_s_concurrent_impl_Promise$Transformation__handleFailure__jl_Throwable__s_concurrent_ExecutionContext__V(this, e$3, e);
  }
  return this;
});
$p.e8 = (function() {
  var x$proxy4 = this.fK;
  if ((x$proxy4 === null)) {
    $m_sr_Scala3RunTime$().bp();
  }
  var x$proxy5 = this.gO;
  if ((x$proxy5 === null)) {
    $m_sr_Scala3RunTime$().bp();
  }
  var x$proxy6 = this.fL;
  if ((x$proxy6 === null)) {
    $m_sr_Scala3RunTime$().bp();
  }
  this.gO = null;
  this.fK = null;
  this.fL = null;
  try {
    var resolvedResult;
    switch (this.fM) {
      case 0: {
        var resolvedResult = null;
        break;
      }
      case 1: {
        var resolvedResult = ((x$proxy4 instanceof $c_s_util_Success) ? new $c_s_util_Success(x$proxy5.b(x$proxy4.s())) : x$proxy4);
        break;
      }
      case 2: {
        if ((x$proxy4 instanceof $c_s_util_Success)) {
          var f = x$proxy5.b(x$proxy4.s());
          if ((f instanceof $c_s_concurrent_impl_Promise$DefaultPromise)) {
            f.je(this, null);
          } else {
            this.iN(f);
          }
          var resolvedResult = null;
        } else {
          var resolvedResult = x$proxy4;
        }
        break;
      }
      case 3: {
        var resolvedResult = $m_s_concurrent_impl_Promise$().gd(x$proxy5.b(x$proxy4));
        break;
      }
      case 4: {
        var f$2 = x$proxy5.b(x$proxy4);
        if ((f$2 instanceof $c_s_concurrent_impl_Promise$DefaultPromise)) {
          f$2.je(this, null);
        } else {
          this.iN(f$2);
        }
        var resolvedResult = null;
        break;
      }
      case 5: {
        x$proxy4.bm(x$proxy5);
        var resolvedResult = null;
        break;
      }
      case 6: {
        x$proxy5.b(x$proxy4);
        var resolvedResult = null;
        break;
      }
      case 7: {
        var resolvedResult = ((x$proxy4 instanceof $c_s_util_Failure) ? $m_s_concurrent_impl_Promise$().gd(x$proxy4.jp(x$proxy5)) : x$proxy4);
        break;
      }
      case 8: {
        if ((x$proxy4 instanceof $c_s_util_Failure)) {
          var f$3 = x$proxy5.bX(x$proxy4.c7, $m_s_concurrent_Future$().mF);
          var resolvedResult = ((f$3 !== $m_s_concurrent_Future$().iz) ? (((f$3 instanceof $c_s_concurrent_impl_Promise$DefaultPromise) ? f$3.je(this, null) : this.iN(f$3)), null) : x$proxy4);
        } else {
          var resolvedResult = x$proxy4;
        }
        break;
      }
      case 9: {
        var resolvedResult = (((x$proxy4 instanceof $c_s_util_Failure) || (!(!x$proxy5.b(x$proxy4.s())))) ? x$proxy4 : $m_s_concurrent_Future$().mE);
        break;
      }
      case 10: {
        var resolvedResult = ((x$proxy4 instanceof $c_s_util_Success) ? new $c_s_util_Success(x$proxy5.bX(x$proxy4.s(), $m_s_concurrent_Future$().mC)) : x$proxy4);
        break;
      }
      default: {
        var resolvedResult = new $c_s_util_Failure(new $c_jl_IllegalStateException(("BUG: encountered transformation promise with illegal type: " + this.fM)));
      }
    }
    if ((resolvedResult !== null)) {
      this.ea(this.L, resolvedResult);
    }
  } catch (e) {
    $p_s_concurrent_impl_Promise$Transformation__handleFailure__jl_Throwable__s_concurrent_ExecutionContext__V(this, ((e instanceof $c_jl_Throwable) ? e : new $c_sjs_js_JavaScriptException(e)), x$proxy6);
  }
});
function $isArrayOf_s_concurrent_impl_Promise$Transformation(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.cw)));
}
var $d_s_concurrent_impl_Promise$Transformation = new $TypeData().i($c_s_concurrent_impl_Promise$Transformation, "scala.concurrent.impl.Promise$Transformation", ({
  cw: 1,
  aY: 1,
  aG: 1,
  a: 1,
  ct: 1,
  cq: 1,
  cs: 1,
  e: 1,
  av: 1,
  aE: 1,
  h1: 1
}));
/** @constructor */
function $c_Lcom_raquo_airstream_misc_CollectStream(parent, fn) {
  this.jU = null;
  this.jT = false;
  this.jV = null;
  this.jQ = null;
  this.jS = null;
  this.jX = false;
  this.gq = null;
  this.jR = null;
  this.jW = 0;
  this.gq = parent;
  this.jR = fn;
  this.jU = (void 0);
  $f_Lcom_raquo_airstream_core_BaseObservable__$init$__V(this);
  $f_Lcom_raquo_airstream_core_WritableObservable__$init$__V(this);
  this.jW = ((1 + parent.gj()) | 0);
}
$p = $c_Lcom_raquo_airstream_misc_CollectStream.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_airstream_misc_CollectStream;
/** @constructor */
function $h_Lcom_raquo_airstream_misc_CollectStream() {
}
$h_Lcom_raquo_airstream_misc_CollectStream.prototype = $p;
$p.e3 = (function() {
  return this.jU;
});
$p.e0 = (function() {
  return $f_Lcom_raquo_airstream_core_Named__defaultDisplayName__T(this);
});
$p.t = (function() {
  return $f_Lcom_raquo_airstream_core_Named__displayName__T(this);
});
$p.g5 = (function() {
  return this.jT;
});
$p.e4 = (function() {
  return this.jV;
});
$p.cu = (function(x$1) {
  this.jT = x$1;
});
$p.g7 = (function(x$1) {
  this.jV = x$1;
});
$p.k = (function(obj) {
  return (this === obj);
});
$p.r = (function() {
  return $systemIdentityHashCode(this);
});
$p.hd = (function(observer) {
});
$p.cV = (function() {
  return this.jQ;
});
$p.cX = (function() {
  return this.jS;
});
$p.ho = (function() {
  return this.jX;
});
$p.f0 = (function(x$1) {
  this.jX = x$1;
});
$p.h1 = (function(x$0) {
  this.jQ = x$0;
});
$p.h2 = (function(x$0) {
  this.jS = x$0;
});
$p.hi = (function() {
  $f_Lcom_raquo_airstream_core_WritableObservable__maybeWillStart__V(this.gq);
});
$p.hf = (function() {
  $f_Lcom_raquo_airstream_common_SingleParentStream__onStart__V(this);
});
$p.hg = (function() {
  $f_Lcom_raquo_airstream_common_SingleParentStream__onStop__V(this);
});
$p.hh = (function(nextValue, transaction) {
  $f_Lcom_raquo_airstream_common_InternalNextErrorObserver__onTry__s_util_Try__Lcom_raquo_airstream_core_Transaction__V(this, nextValue, transaction);
});
$p.gj = (function() {
  return this.jW;
});
$p.jl = (function(nextParentValue, transaction) {
  try {
    var $x_1 = new $c_s_util_Success(this.jR.b(nextParentValue));
  } catch (e) {
    var e$2 = ((e instanceof $c_jl_Throwable) ? e : new $c_sjs_js_JavaScriptException(e));
    matchResult1: {
      var $x_1;
      var x2 = $m_s_util_control_NonFatal$().dF(e$2);
      if ((!x2.c())) {
        var $x_1 = new $c_s_util_Failure(x2.s());
        break matchResult1;
      }
      throw ((e$2 instanceof $c_sjs_js_JavaScriptException) ? e$2.K : e$2);
    }
  }
  $x_1.c8(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((_$1) => {
    $f_Lcom_raquo_airstream_core_WritableStream__fireError__jl_Throwable__Lcom_raquo_airstream_core_Transaction__V(this, _$1, transaction);
  })), new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((nextValue) => {
    if ((!nextValue.c())) {
      $f_Lcom_raquo_airstream_core_WritableStream__fireValue__O__Lcom_raquo_airstream_core_Transaction__V(this, nextValue.s(), transaction);
    }
  })));
});
$p.nZ = (function(nextError, transaction) {
  $f_Lcom_raquo_airstream_core_WritableStream__fireError__jl_Throwable__Lcom_raquo_airstream_core_Transaction__V(this, nextError, transaction);
});
$p.gi = (function() {
  return this;
});
var $d_Lcom_raquo_airstream_misc_CollectStream = new $TypeData().i($c_Lcom_raquo_airstream_misc_CollectStream, "com.raquo.airstream.misc.CollectStream", ({
  cX: 1,
  aj: 1,
  a5: 1,
  ao: 1,
  ap: 1,
  b8: 1,
  b6: 1,
  ar: 1,
  ba: 1,
  az: 1,
  cH: 1,
  cE: 1
}));
/** @constructor */
function $c_Lcom_raquo_airstream_misc_MapSignal(parent, project, recover) {
  this.k1 = null;
  this.k0 = false;
  this.k2 = null;
  this.hu = 0;
  this.jY = null;
  this.jZ = null;
  this.k4 = false;
  this.hv = null;
  this.hw = false;
  this.gr = 0;
  this.cZ = null;
  this.hx = null;
  this.hy = null;
  this.k3 = 0;
  this.cZ = parent;
  this.hx = project;
  this.hy = recover;
  this.k1 = (void 0);
  $f_Lcom_raquo_airstream_core_BaseObservable__$init$__V(this);
  this.hu = 0;
  $f_Lcom_raquo_airstream_core_WritableObservable__$init$__V(this);
  this.hv = (void 0);
  $f_Lcom_raquo_airstream_common_SingleParentSignal__$init$__V(this);
  this.k3 = ((1 + parent.gj()) | 0);
}
$p = $c_Lcom_raquo_airstream_misc_MapSignal.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_airstream_misc_MapSignal;
/** @constructor */
function $h_Lcom_raquo_airstream_misc_MapSignal() {
}
$h_Lcom_raquo_airstream_misc_MapSignal.prototype = $p;
$p.e3 = (function() {
  return this.k1;
});
$p.e0 = (function() {
  return $f_Lcom_raquo_airstream_core_Named__defaultDisplayName__T(this);
});
$p.t = (function() {
  return $f_Lcom_raquo_airstream_core_Named__displayName__T(this);
});
$p.g5 = (function() {
  return this.k0;
});
$p.e4 = (function() {
  return this.k2;
});
$p.cu = (function(x$1) {
  this.k0 = x$1;
});
$p.g7 = (function(x$1) {
  this.k2 = x$1;
});
$p.k = (function(obj) {
  return (this === obj);
});
$p.r = (function() {
  return $systemIdentityHashCode(this);
});
$p.iD = (function() {
  return this.hu;
});
$p.iE = (function(x$1) {
  this.hu = x$1;
});
$p.hd = (function(observer) {
  observer.e5($f_Lcom_raquo_airstream_core_WritableSignal__tryNow__s_util_Try(this));
});
$p.cV = (function() {
  return this.jY;
});
$p.cX = (function() {
  return this.jZ;
});
$p.ho = (function() {
  return this.k4;
});
$p.f0 = (function(x$1) {
  this.k4 = x$1;
});
$p.h1 = (function(x$0) {
  this.jY = x$0;
});
$p.h2 = (function(x$0) {
  this.jZ = x$0;
});
$p.jh = (function() {
  return this.hv;
});
$p.nQ = (function(x$1) {
  this.hv = x$1;
});
$p.ju = (function() {
  return $f_Lcom_raquo_airstream_core_WritableSignal__tryNow__s_util_Try(this);
});
$p.jl = (function(nextValue, transaction) {
  $f_Lcom_raquo_airstream_common_InternalTryObserver__onNext__O__Lcom_raquo_airstream_core_Transaction__V(this, nextValue, transaction);
});
$p.nZ = (function(nextError, transaction) {
  $f_Lcom_raquo_airstream_common_InternalTryObserver__onError__jl_Throwable__Lcom_raquo_airstream_core_Transaction__V(this, nextError, transaction);
});
$p.hi = (function() {
  $f_Lcom_raquo_airstream_common_SingleParentSignal__onWillStart__V(this);
});
$p.hf = (function() {
  $f_Lcom_raquo_airstream_common_SingleParentSignal__onStart__V(this);
});
$p.hg = (function() {
  $f_Lcom_raquo_airstream_common_SingleParentSignal__onStop__V(this);
});
$p.gj = (function() {
  return this.k3;
});
$p.hh = (function(nextParentValue, transaction) {
  $f_Lcom_raquo_airstream_common_SingleParentSignal__onTry__s_util_Try__Lcom_raquo_airstream_core_Transaction__V(this, nextParentValue, transaction);
  nextParentValue.c8(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((nextError) => {
    var this$2 = this.hy;
    if (this$2.c()) {
      $f_Lcom_raquo_airstream_core_WritableSignal__fireError__jl_Throwable__Lcom_raquo_airstream_core_Transaction__V(this, nextError, transaction);
    } else {
      var x0 = this$2.s();
      try {
        var $x_1 = new $c_s_util_Success(x0.bX(nextError, new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((_$1) => null))));
      } catch (e) {
        var e$2 = ((e instanceof $c_jl_Throwable) ? e : new $c_sjs_js_JavaScriptException(e));
        matchResult1: {
          var $x_1;
          var x2 = $m_s_util_control_NonFatal$().dF(e$2);
          if ((!x2.c())) {
            var $x_1 = new $c_s_util_Failure(x2.s());
            break matchResult1;
          }
          throw ((e$2 instanceof $c_sjs_js_JavaScriptException) ? e$2.K : e$2);
        }
      }
      $x_1.c8(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((nextError$3$3) => ((tryError) => {
        $f_Lcom_raquo_airstream_core_WritableSignal__fireError__jl_Throwable__Lcom_raquo_airstream_core_Transaction__V(this, new $c_Lcom_raquo_airstream_core_AirstreamError$ErrorHandlingError(tryError, nextError$3$3), transaction);
      }))(nextError)), new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((nextError$3$4) => ((nextValue) => {
        if ((nextValue === null)) {
          $f_Lcom_raquo_airstream_core_WritableSignal__fireError__jl_Throwable__Lcom_raquo_airstream_core_Transaction__V(this, nextError$3$4, transaction);
        } else if ((!nextValue.c())) {
          $f_Lcom_raquo_airstream_core_WritableSignal__fireValue__O__Lcom_raquo_airstream_core_Transaction__V(this, nextValue.s(), transaction);
        }
      }))(nextError)));
    }
  })), new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((_$3) => {
    $f_Lcom_raquo_airstream_core_WritableSignal__fireTry__s_util_Try__Lcom_raquo_airstream_core_Transaction__V(this, nextParentValue.jg(this.hx), transaction);
  })));
});
$p.iQ = (function() {
  var originalValue = this.cZ.ju().jg(this.hx);
  return originalValue.c8(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((nextError) => {
    var this$2 = this.hy;
    if (this$2.c()) {
      return originalValue;
    } else {
      var x0 = this$2.s();
      try {
        var $x_1 = new $c_s_util_Success(x0.bX(nextError, new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((_$4) => null))));
      } catch (e) {
        var e$2 = ((e instanceof $c_jl_Throwable) ? e : new $c_sjs_js_JavaScriptException(e));
        matchResult1: {
          var $x_1;
          var x2 = $m_s_util_control_NonFatal$().dF(e$2);
          if ((!x2.c())) {
            var $x_1 = new $c_s_util_Failure(x2.s());
            break matchResult1;
          }
          throw ((e$2 instanceof $c_sjs_js_JavaScriptException) ? e$2.K : e$2);
        }
      }
      return $x_1.c8(new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((nextError$7$3) => ((tryError) => new $c_s_util_Failure(new $c_Lcom_raquo_airstream_core_AirstreamError$ErrorHandlingError(tryError, nextError$7$3))))(nextError)), new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((nextValue) => {
        if ((nextValue === null)) {
          return originalValue;
        } else {
          var this$10 = (nextValue.c() ? $m_s_None$() : new $c_s_Some(new $c_s_util_Success(nextValue.s())));
          return (this$10.c() ? originalValue : this$10.s());
        }
      })));
    }
  })), new $c_sjsr_AnonFunction1_$$Lambda$412915ce24663401f4bc24349a746e1dbd693dc1(((_$6) => originalValue)));
});
$p.gi = (function() {
  return this;
});
var $d_Lcom_raquo_airstream_misc_MapSignal = new $TypeData().i($c_Lcom_raquo_airstream_misc_MapSignal, "com.raquo.airstream.misc.MapSignal", ({
  cY: 1,
  aj: 1,
  a5: 1,
  ao: 1,
  ap: 1,
  aB: 1,
  b7: 1,
  ar: 1,
  b9: 1,
  az: 1,
  cF: 1,
  cG: 1
}));
/** @constructor */
function $c_sc_AbstractSeq() {
}
$p = $c_sc_AbstractSeq.prototype = new $h_sc_AbstractIterable();
$p.constructor = $c_sc_AbstractSeq;
/** @constructor */
function $h_sc_AbstractSeq() {
}
$h_sc_AbstractSeq.prototype = $p;
$p.bX = (function(x, default$1) {
  return $f_s_PartialFunction__applyOrElse__O__F1__O(this, x, default$1);
});
$p.cq = (function(f) {
  return $f_sc_SeqOps__distinctBy__F1__O(this, f);
});
$p.jd = (function(idx) {
  return $f_sc_SeqOps__isDefinedAt__I__Z(this, idx);
});
$p.bc = (function(len) {
  return $f_sc_IterableOps__sizeCompare__I__I(this, len);
});
$p.c = (function() {
  return $f_sc_SeqOps__isEmpty__Z(this);
});
$p.eW = (function(that) {
  return $f_sc_SeqOps__sameElements__sc_IterableOnce__Z(this, that);
});
$p.gZ = (function(that) {
  return true;
});
$p.k = (function(o) {
  return $f_sc_Seq__equals__O__Z(this, o);
});
$p.r = (function() {
  return $m_s_util_hashing_MurmurHash3$().ob(this);
});
$p.t = (function() {
  return $f_sc_Iterable__toString__T(this);
});
$p.ca = (function(x) {
  return this.jd((x | 0));
});
/** @constructor */
function $c_sc_AbstractSeqView() {
}
$p = $c_sc_AbstractSeqView.prototype = new $h_sc_AbstractView();
$p.constructor = $c_sc_AbstractSeqView;
/** @constructor */
function $h_sc_AbstractSeqView() {
}
$h_sc_AbstractSeqView.prototype = $p;
$p.cq = (function(f) {
  return $f_sc_SeqOps__distinctBy__F1__O(this, f);
});
$p.bc = (function(len) {
  return $f_sc_IterableOps__sizeCompare__I__I(this, len);
});
$p.c = (function() {
  return $f_sc_SeqOps__isEmpty__Z(this);
});
$p.bq = (function() {
  return "SeqView";
});
function $is_sc_IndexedSeq(obj) {
  return (!(!((obj && obj.$classData) && obj.$classData.n.o)));
}
function $isArrayOf_sc_IndexedSeq(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.o)));
}
function $is_sc_LinearSeq(obj) {
  return (!(!((obj && obj.$classData) && obj.$classData.n.an)));
}
function $isArrayOf_sc_LinearSeq(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.an)));
}
function $f_Lcom_raquo_laminar_api_Laminar__$init$__V($thiz) {
  $thiz.kK = new $c_Lcom_raquo_laminar_api_Laminar$$anon$1();
  $thiz.ot = $m_Lcom_raquo_laminar_receivers_ChildReceiver$();
  $thiz.ou = $m_Lcom_raquo_laminar_receivers_ChildrenReceiver$();
}
/** @constructor */
function $c_sc_AbstractMap() {
}
$p = $c_sc_AbstractMap.prototype = new $h_sc_AbstractIterable();
$p.constructor = $c_sc_AbstractMap;
/** @constructor */
function $h_sc_AbstractMap() {
}
$h_sc_AbstractMap.prototype = $p;
$p.c9 = (function(key, default$1) {
  return $f_sc_MapOps__getOrElse__O__F0__O(this, key, default$1);
});
$p.b = (function(key) {
  return $f_sc_MapOps__apply__O__O(this, key);
});
$p.bX = (function(x, default$1) {
  return $f_sc_MapOps__applyOrElse__O__F1__O(this, x, default$1);
});
$p.e1 = (function(f) {
  $f_sc_MapOps__foreachEntry__F2__V(this, f);
});
$p.nl = (function(key) {
  return $f_sc_MapOps__default__O__O(this, key);
});
$p.bl = (function(key) {
  return $f_sc_MapOps__contains__O__Z(this, key);
});
$p.ca = (function(key) {
  return this.bl(key);
});
$p.dy = (function(sb, start, sep, end) {
  return $f_sc_MapOps__addString__scm_StringBuilder__T__T__T__scm_StringBuilder(this, sb, start, sep, end);
});
$p.eR = (function(coll) {
  return this.g6().ag(coll);
});
$p.k = (function(o) {
  return $f_sc_Map__equals__O__Z(this, o);
});
$p.r = (function() {
  return $m_s_util_hashing_MurmurHash3$().qA(this);
});
$p.bq = (function() {
  return "Map";
});
$p.t = (function() {
  return $f_sc_Iterable__toString__T(this);
});
function $ct_sc_SeqView$Id__sc_SeqOps__($thiz, underlying) {
  $thiz.dQ = underlying;
  return $thiz;
}
/** @constructor */
function $c_sc_SeqView$Id() {
  this.dQ = null;
}
$p = $c_sc_SeqView$Id.prototype = new $h_sc_AbstractSeqView();
$p.constructor = $c_sc_SeqView$Id;
/** @constructor */
function $h_sc_SeqView$Id() {
}
$h_sc_SeqView$Id.prototype = $p;
$p.v = (function(idx) {
  return this.dQ.v(idx);
});
$p.q = (function() {
  return this.dQ.q();
});
$p.i = (function() {
  return this.dQ.i();
});
$p.x = (function() {
  return this.dQ.x();
});
$p.c = (function() {
  return this.dQ.c();
});
var $d_sc_SeqView$Id = new $TypeData().i($c_sc_SeqView$Id, "scala.collection.SeqView$Id", ({
  bO: 1,
  aJ: 1,
  am: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  a: 1,
  ac: 1,
  l: 1,
  aM: 1
}));
/** @constructor */
function $c_Lcom_raquo_laminar_api_package$$anon$1() {
  this.kL = null;
  this.kM = false;
  this.kC = null;
  this.kD = false;
  this.kP = null;
  this.kQ = false;
  this.kN = null;
  this.kO = false;
  this.kx = null;
  this.ky = false;
  this.l5 = null;
  this.l6 = false;
  this.kX = null;
  this.kY = false;
  this.kZ = null;
  this.l0 = false;
  this.l3 = null;
  this.l4 = false;
  this.kI = null;
  this.kJ = false;
  this.lb = null;
  this.lc = false;
  this.ld = null;
  this.le = false;
  this.lj = null;
  this.lk = false;
  this.ll = null;
  this.lm = false;
  this.lf = null;
  this.lg = false;
  this.lh = null;
  this.li = false;
  this.kE = null;
  this.kF = false;
  this.l7 = null;
  this.l8 = false;
  this.kz = null;
  this.kA = false;
  this.lp = null;
  this.lq = false;
  this.kG = null;
  this.kH = false;
  this.l1 = null;
  this.l2 = false;
  this.kT = null;
  this.kU = false;
  this.kR = null;
  this.kS = false;
  this.kV = null;
  this.kW = false;
  this.kB = null;
  this.dL = null;
  this.dK = null;
  this.os = null;
  this.kv = null;
  this.kw = false;
  this.l9 = null;
  this.la = false;
  this.kK = null;
  this.ln = null;
  this.lo = false;
  this.ot = null;
  this.ou = null;
  $f_Lcom_raquo_laminar_defs_complex_ComplexHtmlKeys__$init$__V(this);
  $f_Lcom_raquo_laminar_api_MountHooks__$init$__V(this);
  $f_Lcom_raquo_laminar_api_AirstreamAliases__$init$__V(this);
  $f_Lcom_raquo_laminar_api_LaminarAliases__$init$__V(this);
  $f_Lcom_raquo_laminar_api_Laminar__$init$__V(this);
}
$p = $c_Lcom_raquo_laminar_api_package$$anon$1.prototype = new $h_O();
$p.constructor = $c_Lcom_raquo_laminar_api_package$$anon$1;
/** @constructor */
function $h_Lcom_raquo_laminar_api_package$$anon$1() {
}
$h_Lcom_raquo_laminar_api_package$$anon$1.prototype = $p;
$p.qg = (function() {
  if ((!this.kM)) {
    this.kL = new $c_Lcom_raquo_laminar_tags_HtmlTag("h1", false);
    this.kM = true;
  }
  return this.kL;
});
$p.pt = (function() {
  if ((!this.kD)) {
    this.kC = new $c_Lcom_raquo_laminar_tags_HtmlTag("code", false);
    this.kD = true;
  }
  return this.kC;
});
$p.nN = (function() {
  if ((!this.kQ)) {
    this.kP = new $c_Lcom_raquo_laminar_tags_HtmlTag("label", false);
    this.kQ = true;
  }
  return this.kP;
});
$p.qn = (function() {
  if ((!this.kO)) {
    this.kN = new $c_Lcom_raquo_laminar_tags_HtmlTag("input", true);
    this.kO = true;
  }
  return this.kN;
});
$p.po = (function() {
  if ((!this.ky)) {
    this.kx = new $c_Lcom_raquo_laminar_tags_HtmlTag("button", false);
    this.ky = true;
  }
  return this.kx;
});
$p.r9 = (function() {
  if ((!this.l6)) {
    this.l5 = new $c_Lcom_raquo_laminar_tags_HtmlTag("select", false);
    this.l6 = true;
  }
  return this.l5;
});
$p.qL = (function() {
  if ((!this.kY)) {
    this.kX = new $c_Lcom_raquo_laminar_tags_HtmlTag("option", false);
    this.kY = true;
  }
  return this.kX;
});
$p.jn = (function() {
  if ((!this.l0)) {
    this.kZ = new $c_Lcom_raquo_laminar_tags_HtmlTag("p", false);
    this.l0 = true;
  }
  return this.kZ;
});
$p.qO = (function() {
  if ((!this.l4)) {
    this.l3 = new $c_Lcom_raquo_laminar_tags_HtmlTag("pre", false);
    this.l4 = true;
  }
  return this.l3;
});
$p.iS = (function() {
  if ((!this.kJ)) {
    this.kI = new $c_Lcom_raquo_laminar_tags_HtmlTag("div", false);
    this.kJ = true;
  }
  return this.kI;
});
$p.rr = (function() {
  if ((!this.lc)) {
    this.lb = new $c_Lcom_raquo_laminar_tags_HtmlTag("table", false);
    this.lc = true;
  }
  return this.lb;
});
$p.ru = (function() {
  if ((!this.le)) {
    this.ld = new $c_Lcom_raquo_laminar_tags_HtmlTag("tbody", false);
    this.le = true;
  }
  return this.ld;
});
$p.ry = (function() {
  if ((!this.lk)) {
    this.lj = new $c_Lcom_raquo_laminar_tags_HtmlTag("thead", false);
    this.lk = true;
  }
  return this.lj;
});
$p.oj = (function() {
  if ((!this.lm)) {
    this.ll = new $c_Lcom_raquo_laminar_tags_HtmlTag("tr", false);
    this.lm = true;
  }
  return this.ll;
});
$p.rv = (function() {
  if ((!this.lg)) {
    this.lf = new $c_Lcom_raquo_laminar_tags_HtmlTag("td", false);
    this.lg = true;
  }
  return this.lf;
});
$p.rx = (function() {
  if ((!this.li)) {
    this.lh = new $c_Lcom_raquo_laminar_tags_HtmlTag("th", false);
    this.li = true;
  }
  return this.lh;
});
$p.pI = (function() {
  if ((!this.kF)) {
    this.kE = new $c_Lcom_raquo_laminar_tags_HtmlTag("details", false);
    this.kF = true;
  }
  return this.kE;
});
$p.rl = (function() {
  if ((!this.l8)) {
    this.l7 = new $c_Lcom_raquo_laminar_tags_HtmlTag("summary", false);
    this.l8 = true;
  }
  return this.l7;
});
$p.pq = (function() {
  if ((!this.kA)) {
    this.kz = new $c_Lcom_raquo_laminar_keys_HtmlProp("checked", $m_Lcom_raquo_laminar_codecs_package$().hH);
    this.kA = true;
  }
  return this.kz;
});
$p.hn = (function() {
  if ((!this.lq)) {
    this.lp = new $c_Lcom_raquo_laminar_keys_HtmlProp("value", $m_Lcom_raquo_laminar_codecs_package$().f8);
    this.lq = true;
  }
  return this.lp;
});
$p.pK = (function() {
  if ((!this.kH)) {
    this.kG = new $c_Lcom_raquo_laminar_keys_HtmlProp("disabled", $m_Lcom_raquo_laminar_codecs_package$().hH);
    this.kH = true;
  }
  return this.kG;
});
$p.qN = (function() {
  if ((!this.l2)) {
    this.l1 = new $c_Lcom_raquo_laminar_keys_HtmlProp("placeholder", $m_Lcom_raquo_laminar_codecs_package$().f8);
    this.l2 = true;
  }
  return this.l1;
});
$p.nW = (function() {
  if ((!this.kU)) {
    this.kT = new $c_Lcom_raquo_laminar_keys_EventProp("click");
    this.kU = true;
  }
  return this.kT;
});
$p.nV = (function() {
  if ((!this.kS)) {
    this.kR = new $c_Lcom_raquo_laminar_keys_EventProp("change");
    this.kS = true;
  }
  return this.kR;
});
$p.he = (function() {
  if ((!this.kW)) {
    this.kV = new $c_Lcom_raquo_laminar_keys_EventProp("input");
    this.kW = true;
  }
  return this.kV;
});
$p.oQ = (function() {
  if ((!this.kw)) {
    this.kv = new $c_Lcom_raquo_laminar_keys_CompositeKey$CompositeValueMappers$StringValueMapper$(this);
    this.kw = true;
  }
  return this.kv;
});
$p.rm = (function() {
  if ((!this.la)) {
    this.l9 = new $c_Lcom_raquo_laminar_api_Laminar$svg$(this);
    this.la = true;
  }
  return this.l9;
});
$p.rG = (function() {
  if ((!this.lo)) {
    this.ln = new $c_Lcom_raquo_laminar_api_Laminar$unsafeWindowOwner$(this);
    this.lo = true;
  }
  return this.ln;
});
var $d_Lcom_raquo_laminar_api_package$$anon$1 = new $TypeData().i($c_Lcom_raquo_laminar_api_package$$anon$1, "com.raquo.laminar.api.package$$anon$1", ({
  dr: 1,
  dB: 1,
  du: 1,
  dz: 1,
  bf: 1,
  dA: 1,
  dw: 1,
  dp: 1,
  di: 1,
  dn: 1,
  bd: 1,
  bg: 1,
  bc: 1,
  dj: 1
}));
function $is_sci_Map(obj) {
  return (!(!((obj && obj.$classData) && obj.$classData.n.a3)));
}
function $isArrayOf_sci_Map(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.a3)));
}
/** @constructor */
function $c_sc_AbstractIndexedSeqView() {
}
$p = $c_sc_AbstractIndexedSeqView.prototype = new $h_sc_AbstractSeqView();
$p.constructor = $c_sc_AbstractIndexedSeqView;
/** @constructor */
function $h_sc_AbstractIndexedSeqView() {
}
$h_sc_AbstractIndexedSeqView.prototype = $p;
$p.bc = (function(len) {
  var x = this.q();
  return ((x === len) ? 0 : ((x < len) ? (-1) : 1));
});
$p.x = (function() {
  return this.q();
});
$p.bq = (function() {
  return "IndexedSeqView";
});
/** @constructor */
function $c_sc_IndexedSeqView$Id(underlying) {
  this.dQ = null;
  $ct_sc_SeqView$Id__sc_SeqOps__(this, underlying);
}
$p = $c_sc_IndexedSeqView$Id.prototype = new $h_sc_SeqView$Id();
$p.constructor = $c_sc_IndexedSeqView$Id;
/** @constructor */
function $h_sc_IndexedSeqView$Id() {
}
$h_sc_IndexedSeqView$Id.prototype = $p;
$p.bc = (function(len) {
  var x = this.q();
  return ((x === len) ? 0 : ((x < len) ? (-1) : 1));
});
$p.x = (function() {
  return this.q();
});
$p.i = (function() {
  return $ct_sc_IndexedSeqView$IndexedSeqViewIterator__sc_IndexedSeqView__(new $c_sc_IndexedSeqView$IndexedSeqViewIterator(), this);
});
$p.bq = (function() {
  return "IndexedSeqView";
});
var $d_sc_IndexedSeqView$Id = new $TypeData().i($c_sc_IndexedSeqView$Id, "scala.collection.IndexedSeqView$Id", ({
  fp: 1,
  bO: 1,
  aJ: 1,
  am: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  a: 1,
  ac: 1,
  l: 1,
  aM: 1,
  p: 1,
  bK: 1
}));
/** @constructor */
function $c_sci_AbstractSeq() {
}
$p = $c_sci_AbstractSeq.prototype = new $h_sc_AbstractSeq();
$p.constructor = $c_sci_AbstractSeq;
/** @constructor */
function $h_sci_AbstractSeq() {
}
$h_sci_AbstractSeq.prototype = $p;
/** @constructor */
function $c_scm_ArrayBufferView(underlying, mutationCount) {
  this.ir = null;
  this.mo = null;
  this.ir = underlying;
  this.mo = mutationCount;
}
$p = $c_scm_ArrayBufferView.prototype = new $h_sc_AbstractIndexedSeqView();
$p.constructor = $c_scm_ArrayBufferView;
/** @constructor */
function $h_scm_ArrayBufferView() {
}
$h_scm_ArrayBufferView.prototype = $p;
$p.v = (function(n) {
  return this.ir.v(n);
});
$p.q = (function() {
  return this.ir.aT;
});
$p.bZ = (function() {
  return "ArrayBufferView";
});
$p.i = (function() {
  return new $c_scm_CheckedIndexedSeqView$CheckedIterator(this, this.mo);
});
var $d_scm_ArrayBufferView = new $TypeData().i($c_scm_ArrayBufferView, "scala.collection.mutable.ArrayBufferView", ({
  gD: 1,
  fi: 1,
  aJ: 1,
  am: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  a: 1,
  ac: 1,
  l: 1,
  aM: 1,
  p: 1,
  bK: 1
}));
/** @constructor */
function $c_sci_AbstractMap() {
}
$p = $c_sci_AbstractMap.prototype = new $h_sc_AbstractMap();
$p.constructor = $c_sci_AbstractMap;
/** @constructor */
function $h_sci_AbstractMap() {
}
$h_sci_AbstractMap.prototype = $p;
$p.bn = (function() {
  return $m_sci_Iterable$();
});
$p.g6 = (function() {
  return $m_sci_Map$();
});
function $f_sci_IndexedSeq__canEqual__O__Z($thiz, that) {
  return ($is_sci_IndexedSeq(that) ? ($thiz.q() === that.q()) : true);
}
function $f_sci_IndexedSeq__sameElements__sc_IterableOnce__Z($thiz, o) {
  if ($is_sci_IndexedSeq(o)) {
    if (($thiz === o)) {
      return true;
    } else {
      var length = $thiz.q();
      var equal = (length === o.q());
      if (equal) {
        var index = 0;
        var a = $thiz.gX();
        var b = o.gX();
        var preferredLength = ((a < b) ? a : b);
        var hi = (length >> 31);
        var hi$1 = (preferredLength >> 31);
        var lo = (preferredLength << 1);
        var hi$2 = (((preferredLength >>> 31) | 0) | (hi$1 << 1));
        if (((hi === hi$2) ? ((length >>> 0) > (lo >>> 0)) : (hi > hi$2))) {
          var maxApplyCompare = preferredLength;
        } else {
          var maxApplyCompare = length;
        }
        while (((index < maxApplyCompare) && equal)) {
          equal = $m_sr_BoxesRunTime$().j($thiz.v(index), o.v(index));
          index = ((1 + index) | 0);
        }
        if (((index < length) && equal)) {
          var thisIt = $thiz.i().dC(index);
          var thatIt = o.i().dC(index);
          while ((equal && thisIt.m())) {
            equal = $m_sr_BoxesRunTime$().j(thisIt.g(), thatIt.g());
          }
        }
      }
      return equal;
    }
  } else {
    return $f_sc_SeqOps__sameElements__sc_IterableOnce__Z($thiz, o);
  }
}
function $is_sci_IndexedSeq(obj) {
  return (!(!((obj && obj.$classData) && obj.$classData.n.y)));
}
function $isArrayOf_sci_IndexedSeq(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.y)));
}
function $isArrayOf_sci_SeqMap$SeqMap1(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.gi)));
}
function $isArrayOf_sci_SeqMap$SeqMap2(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.gj)));
}
function $isArrayOf_sci_SeqMap$SeqMap3(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.gk)));
}
function $isArrayOf_sci_SeqMap$SeqMap4(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.gl)));
}
/** @constructor */
function $c_scm_AbstractSeq() {
}
$p = $c_scm_AbstractSeq.prototype = new $h_sc_AbstractSeq();
$p.constructor = $c_scm_AbstractSeq;
/** @constructor */
function $h_scm_AbstractSeq() {
}
$h_scm_AbstractSeq.prototype = $p;
/** @constructor */
function $c_sci_Map$EmptyMap$() {
}
$p = $c_sci_Map$EmptyMap$.prototype = new $h_sci_AbstractMap();
$p.constructor = $c_sci_Map$EmptyMap$;
/** @constructor */
function $h_sci_Map$EmptyMap$() {
}
$h_sci_Map$EmptyMap$.prototype = $p;
$p.ax = (function() {
  return 0;
});
$p.x = (function() {
  return 0;
});
$p.c = (function() {
  return true;
});
$p.iJ = (function(key) {
  throw $ct_ju_NoSuchElementException__T__(new $c_ju_NoSuchElementException(), ("key not found: " + key));
});
$p.bl = (function(key) {
  return false;
});
$p.cr = (function(key) {
  return $m_s_None$();
});
$p.c9 = (function(key, default$1) {
  return default$1.F();
});
$p.i = (function() {
  return $m_sc_Iterator$().O;
});
$p.b = (function(key) {
  this.iJ(key);
});
$p.cd = (function(key, value) {
  return new $c_sci_Map$Map1(key, value);
});
var $d_sci_Map$EmptyMap$ = new $TypeData().i($c_sci_Map$EmptyMap$, "scala.collection.immutable.Map$EmptyMap$", ({
  g3: 1,
  ad: 1,
  a9: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  ab: 1,
  aa: 1,
  d: 1,
  a2: 1,
  r: 1,
  af: 1,
  a3: 1,
  a: 1
}));
var $n_sci_Map$EmptyMap$;
function $m_sci_Map$EmptyMap$() {
  if ((!$n_sci_Map$EmptyMap$)) {
    $n_sci_Map$EmptyMap$ = new $c_sci_Map$EmptyMap$();
  }
  return $n_sci_Map$EmptyMap$;
}
/** @constructor */
function $c_sci_Map$WithDefault(underlying, defaultValue) {
  this.dj = null;
  this.gK = null;
  this.dj = underlying;
  this.gK = defaultValue;
}
$p = $c_sci_Map$WithDefault.prototype = new $h_sci_AbstractMap();
$p.constructor = $c_sci_Map$WithDefault;
/** @constructor */
function $h_sci_Map$WithDefault() {
}
$h_sci_Map$WithDefault.prototype = $p;
$p.cr = (function(key) {
  return this.dj.cr(key);
});
$p.nl = (function(key) {
  return this.gK.b(key);
});
$p.bn = (function() {
  return this.dj.bn();
});
$p.i = (function() {
  return this.dj.i();
});
$p.c = (function() {
  return this.dj.c();
});
$p.g6 = (function() {
  return this.dj.g6();
});
$p.rH = (function(key, value) {
  return new $c_sci_Map$WithDefault(this.dj.cd(key, value), this.gK);
});
$p.q6 = (function(coll) {
  return new $c_sci_Map$WithDefault(this.dj.g6().ag(coll), this.gK);
});
$p.cd = (function(key, value) {
  return this.rH(key, value);
});
$p.eR = (function(coll) {
  return this.q6(coll);
});
var $d_sci_Map$WithDefault = new $TypeData().i($c_sci_Map$WithDefault, "scala.collection.immutable.Map$WithDefault", ({
  ga: 1,
  ad: 1,
  a9: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  ab: 1,
  aa: 1,
  d: 1,
  a2: 1,
  r: 1,
  af: 1,
  a3: 1,
  a: 1
}));
/** @constructor */
function $c_sci_Map$Map1(key1, value1) {
  this.c5 = null;
  this.de = null;
  this.c5 = key1;
  this.de = value1;
}
$p = $c_sci_Map$Map1.prototype = new $h_sci_AbstractMap();
$p.constructor = $c_sci_Map$Map1;
/** @constructor */
function $h_sci_Map$Map1() {
}
$h_sci_Map$Map1.prototype = $p;
$p.ax = (function() {
  return 1;
});
$p.x = (function() {
  return 1;
});
$p.c = (function() {
  return false;
});
$p.b = (function(key) {
  if ($m_sr_BoxesRunTime$().j(key, this.c5)) {
    return this.de;
  } else {
    throw $ct_ju_NoSuchElementException__T__(new $c_ju_NoSuchElementException(), ("key not found: " + key));
  }
});
$p.bl = (function(key) {
  return $m_sr_BoxesRunTime$().j(key, this.c5);
});
$p.cr = (function(key) {
  return ($m_sr_BoxesRunTime$().j(key, this.c5) ? new $c_s_Some(this.de) : $m_s_None$());
});
$p.c9 = (function(key, default$1) {
  return ($m_sr_BoxesRunTime$().j(key, this.c5) ? this.de : default$1.F());
});
$p.i = (function() {
  return new $c_sc_Iterator$$anon$20(new $c_T2(this.c5, this.de));
});
$p.eb = (function(key, value) {
  return ($m_sr_BoxesRunTime$().j(key, this.c5) ? new $c_sci_Map$Map1(this.c5, value) : new $c_sci_Map$Map2(this.c5, this.de, key, value));
});
$p.eQ = (function(p) {
  return (!(!p.b(new $c_T2(this.c5, this.de))));
});
$p.r = (function() {
  var a = 0;
  var b = 0;
  var c = 1;
  var h = $m_s_util_hashing_MurmurHash3$().cc(this.c5, this.de);
  a = ((a + h) | 0);
  b = (b ^ h);
  c = Math.imul(c, (1 | h));
  h = $m_s_util_hashing_MurmurHash3$().dx;
  h = $m_s_util_hashing_MurmurHash3$().w(h, a);
  h = $m_s_util_hashing_MurmurHash3$().w(h, b);
  h = $m_s_util_hashing_MurmurHash3$().cY(h, c);
  return $m_s_util_hashing_MurmurHash3$().ar(h, 1);
});
$p.cd = (function(key, value) {
  return this.eb(key, value);
});
function $isArrayOf_sci_Map$Map1(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.c6)));
}
var $d_sci_Map$Map1 = new $TypeData().i($c_sci_Map$Map1, "scala.collection.immutable.Map$Map1", ({
  c6: 1,
  ad: 1,
  a9: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  ab: 1,
  aa: 1,
  d: 1,
  a2: 1,
  r: 1,
  af: 1,
  a3: 1,
  k: 1,
  a: 1
}));
/** @constructor */
function $c_sci_Map$Map2(key1, value1, key2, value2) {
  this.bN = null;
  this.cI = null;
  this.bO = null;
  this.cJ = null;
  this.bN = key1;
  this.cI = value1;
  this.bO = key2;
  this.cJ = value2;
}
$p = $c_sci_Map$Map2.prototype = new $h_sci_AbstractMap();
$p.constructor = $c_sci_Map$Map2;
/** @constructor */
function $h_sci_Map$Map2() {
}
$h_sci_Map$Map2.prototype = $p;
$p.ax = (function() {
  return 2;
});
$p.x = (function() {
  return 2;
});
$p.c = (function() {
  return false;
});
$p.b = (function(key) {
  if ($m_sr_BoxesRunTime$().j(key, this.bN)) {
    return this.cI;
  } else if ($m_sr_BoxesRunTime$().j(key, this.bO)) {
    return this.cJ;
  } else {
    throw $ct_ju_NoSuchElementException__T__(new $c_ju_NoSuchElementException(), ("key not found: " + key));
  }
});
$p.bl = (function(key) {
  return ($m_sr_BoxesRunTime$().j(key, this.bN) || $m_sr_BoxesRunTime$().j(key, this.bO));
});
$p.cr = (function(key) {
  return ($m_sr_BoxesRunTime$().j(key, this.bN) ? new $c_s_Some(this.cI) : ($m_sr_BoxesRunTime$().j(key, this.bO) ? new $c_s_Some(this.cJ) : $m_s_None$()));
});
$p.c9 = (function(key, default$1) {
  return ($m_sr_BoxesRunTime$().j(key, this.bN) ? this.cI : ($m_sr_BoxesRunTime$().j(key, this.bO) ? this.cJ : default$1.F()));
});
$p.i = (function() {
  return new $c_sci_Map$Map2$$anon$1(this);
});
$p.eb = (function(key, value) {
  return ($m_sr_BoxesRunTime$().j(key, this.bN) ? new $c_sci_Map$Map2(this.bN, value, this.bO, this.cJ) : ($m_sr_BoxesRunTime$().j(key, this.bO) ? new $c_sci_Map$Map2(this.bN, this.cI, this.bO, value) : new $c_sci_Map$Map3(this.bN, this.cI, this.bO, this.cJ, key, value)));
});
$p.eQ = (function(p) {
  return ((!(!p.b(new $c_T2(this.bN, this.cI)))) && (!(!p.b(new $c_T2(this.bO, this.cJ)))));
});
$p.r = (function() {
  var a = 0;
  var b = 0;
  var c = 1;
  var h = $m_s_util_hashing_MurmurHash3$().cc(this.bN, this.cI);
  a = ((a + h) | 0);
  b = (b ^ h);
  c = Math.imul(c, (1 | h));
  h = $m_s_util_hashing_MurmurHash3$().cc(this.bO, this.cJ);
  a = ((a + h) | 0);
  b = (b ^ h);
  c = Math.imul(c, (1 | h));
  h = $m_s_util_hashing_MurmurHash3$().dx;
  h = $m_s_util_hashing_MurmurHash3$().w(h, a);
  h = $m_s_util_hashing_MurmurHash3$().w(h, b);
  h = $m_s_util_hashing_MurmurHash3$().cY(h, c);
  return $m_s_util_hashing_MurmurHash3$().ar(h, 2);
});
$p.cd = (function(key, value) {
  return this.eb(key, value);
});
function $isArrayOf_sci_Map$Map2(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.c7)));
}
var $d_sci_Map$Map2 = new $TypeData().i($c_sci_Map$Map2, "scala.collection.immutable.Map$Map2", ({
  c7: 1,
  ad: 1,
  a9: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  ab: 1,
  aa: 1,
  d: 1,
  a2: 1,
  r: 1,
  af: 1,
  a3: 1,
  k: 1,
  a: 1
}));
/** @constructor */
function $c_sci_Map$Map3(key1, value1, key2, value2, key3, value3) {
  this.bD = null;
  this.ci = null;
  this.bE = null;
  this.cj = null;
  this.bF = null;
  this.ck = null;
  this.bD = key1;
  this.ci = value1;
  this.bE = key2;
  this.cj = value2;
  this.bF = key3;
  this.ck = value3;
}
$p = $c_sci_Map$Map3.prototype = new $h_sci_AbstractMap();
$p.constructor = $c_sci_Map$Map3;
/** @constructor */
function $h_sci_Map$Map3() {
}
$h_sci_Map$Map3.prototype = $p;
$p.ax = (function() {
  return 3;
});
$p.x = (function() {
  return 3;
});
$p.c = (function() {
  return false;
});
$p.b = (function(key) {
  if ($m_sr_BoxesRunTime$().j(key, this.bD)) {
    return this.ci;
  } else if ($m_sr_BoxesRunTime$().j(key, this.bE)) {
    return this.cj;
  } else if ($m_sr_BoxesRunTime$().j(key, this.bF)) {
    return this.ck;
  } else {
    throw $ct_ju_NoSuchElementException__T__(new $c_ju_NoSuchElementException(), ("key not found: " + key));
  }
});
$p.bl = (function(key) {
  return (($m_sr_BoxesRunTime$().j(key, this.bD) || $m_sr_BoxesRunTime$().j(key, this.bE)) || $m_sr_BoxesRunTime$().j(key, this.bF));
});
$p.cr = (function(key) {
  return ($m_sr_BoxesRunTime$().j(key, this.bD) ? new $c_s_Some(this.ci) : ($m_sr_BoxesRunTime$().j(key, this.bE) ? new $c_s_Some(this.cj) : ($m_sr_BoxesRunTime$().j(key, this.bF) ? new $c_s_Some(this.ck) : $m_s_None$())));
});
$p.c9 = (function(key, default$1) {
  return ($m_sr_BoxesRunTime$().j(key, this.bD) ? this.ci : ($m_sr_BoxesRunTime$().j(key, this.bE) ? this.cj : ($m_sr_BoxesRunTime$().j(key, this.bF) ? this.ck : default$1.F())));
});
$p.i = (function() {
  return new $c_sci_Map$Map3$$anon$4(this);
});
$p.eb = (function(key, value) {
  return ($m_sr_BoxesRunTime$().j(key, this.bD) ? new $c_sci_Map$Map3(this.bD, value, this.bE, this.cj, this.bF, this.ck) : ($m_sr_BoxesRunTime$().j(key, this.bE) ? new $c_sci_Map$Map3(this.bD, this.ci, this.bE, value, this.bF, this.ck) : ($m_sr_BoxesRunTime$().j(key, this.bF) ? new $c_sci_Map$Map3(this.bD, this.ci, this.bE, this.cj, this.bF, value) : new $c_sci_Map$Map4(this.bD, this.ci, this.bE, this.cj, this.bF, this.ck, key, value))));
});
$p.eQ = (function(p) {
  return (((!(!p.b(new $c_T2(this.bD, this.ci)))) && (!(!p.b(new $c_T2(this.bE, this.cj))))) && (!(!p.b(new $c_T2(this.bF, this.ck)))));
});
$p.r = (function() {
  var a = 0;
  var b = 0;
  var c = 1;
  var h = $m_s_util_hashing_MurmurHash3$().cc(this.bD, this.ci);
  a = ((a + h) | 0);
  b = (b ^ h);
  c = Math.imul(c, (1 | h));
  h = $m_s_util_hashing_MurmurHash3$().cc(this.bE, this.cj);
  a = ((a + h) | 0);
  b = (b ^ h);
  c = Math.imul(c, (1 | h));
  h = $m_s_util_hashing_MurmurHash3$().cc(this.bF, this.ck);
  a = ((a + h) | 0);
  b = (b ^ h);
  c = Math.imul(c, (1 | h));
  h = $m_s_util_hashing_MurmurHash3$().dx;
  h = $m_s_util_hashing_MurmurHash3$().w(h, a);
  h = $m_s_util_hashing_MurmurHash3$().w(h, b);
  h = $m_s_util_hashing_MurmurHash3$().cY(h, c);
  return $m_s_util_hashing_MurmurHash3$().ar(h, 3);
});
$p.cd = (function(key, value) {
  return this.eb(key, value);
});
function $isArrayOf_sci_Map$Map3(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.c8)));
}
var $d_sci_Map$Map3 = new $TypeData().i($c_sci_Map$Map3, "scala.collection.immutable.Map$Map3", ({
  c8: 1,
  ad: 1,
  a9: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  ab: 1,
  aa: 1,
  d: 1,
  a2: 1,
  r: 1,
  af: 1,
  a3: 1,
  k: 1,
  a: 1
}));
/** @constructor */
function $c_sci_Map$Map4(key1, value1, key2, value2, key3, value3, key4, value4) {
  this.be = null;
  this.bP = null;
  this.bf = null;
  this.bQ = null;
  this.bg = null;
  this.bR = null;
  this.bh = null;
  this.bS = null;
  this.be = key1;
  this.bP = value1;
  this.bf = key2;
  this.bQ = value2;
  this.bg = key3;
  this.bR = value3;
  this.bh = key4;
  this.bS = value4;
}
$p = $c_sci_Map$Map4.prototype = new $h_sci_AbstractMap();
$p.constructor = $c_sci_Map$Map4;
/** @constructor */
function $h_sci_Map$Map4() {
}
$h_sci_Map$Map4.prototype = $p;
$p.ax = (function() {
  return 4;
});
$p.x = (function() {
  return 4;
});
$p.c = (function() {
  return false;
});
$p.b = (function(key) {
  if ($m_sr_BoxesRunTime$().j(key, this.be)) {
    return this.bP;
  } else if ($m_sr_BoxesRunTime$().j(key, this.bf)) {
    return this.bQ;
  } else if ($m_sr_BoxesRunTime$().j(key, this.bg)) {
    return this.bR;
  } else if ($m_sr_BoxesRunTime$().j(key, this.bh)) {
    return this.bS;
  } else {
    throw $ct_ju_NoSuchElementException__T__(new $c_ju_NoSuchElementException(), ("key not found: " + key));
  }
});
$p.bl = (function(key) {
  return ((($m_sr_BoxesRunTime$().j(key, this.be) || $m_sr_BoxesRunTime$().j(key, this.bf)) || $m_sr_BoxesRunTime$().j(key, this.bg)) || $m_sr_BoxesRunTime$().j(key, this.bh));
});
$p.cr = (function(key) {
  return ($m_sr_BoxesRunTime$().j(key, this.be) ? new $c_s_Some(this.bP) : ($m_sr_BoxesRunTime$().j(key, this.bf) ? new $c_s_Some(this.bQ) : ($m_sr_BoxesRunTime$().j(key, this.bg) ? new $c_s_Some(this.bR) : ($m_sr_BoxesRunTime$().j(key, this.bh) ? new $c_s_Some(this.bS) : $m_s_None$()))));
});
$p.c9 = (function(key, default$1) {
  return ($m_sr_BoxesRunTime$().j(key, this.be) ? this.bP : ($m_sr_BoxesRunTime$().j(key, this.bf) ? this.bQ : ($m_sr_BoxesRunTime$().j(key, this.bg) ? this.bR : ($m_sr_BoxesRunTime$().j(key, this.bh) ? this.bS : default$1.F()))));
});
$p.i = (function() {
  return new $c_sci_Map$Map4$$anon$7(this);
});
$p.eb = (function(key, value) {
  return ($m_sr_BoxesRunTime$().j(key, this.be) ? new $c_sci_Map$Map4(this.be, value, this.bf, this.bQ, this.bg, this.bR, this.bh, this.bS) : ($m_sr_BoxesRunTime$().j(key, this.bf) ? new $c_sci_Map$Map4(this.be, this.bP, this.bf, value, this.bg, this.bR, this.bh, this.bS) : ($m_sr_BoxesRunTime$().j(key, this.bg) ? new $c_sci_Map$Map4(this.be, this.bP, this.bf, this.bQ, this.bg, value, this.bh, this.bS) : ($m_sr_BoxesRunTime$().j(key, this.bh) ? new $c_sci_Map$Map4(this.be, this.bP, this.bf, this.bQ, this.bg, this.bR, this.bh, value) : $m_sci_HashMap$().ij.eZ(this.be, this.bP).eZ(this.bf, this.bQ).eZ(this.bg, this.bR).eZ(this.bh, this.bS).eZ(key, value)))));
});
$p.eQ = (function(p) {
  return ((((!(!p.b(new $c_T2(this.be, this.bP)))) && (!(!p.b(new $c_T2(this.bf, this.bQ))))) && (!(!p.b(new $c_T2(this.bg, this.bR))))) && (!(!p.b(new $c_T2(this.bh, this.bS)))));
});
$p.pn = (function(builder) {
  return builder.dY(this.be, this.bP).dY(this.bf, this.bQ).dY(this.bg, this.bR).dY(this.bh, this.bS);
});
$p.r = (function() {
  var a = 0;
  var b = 0;
  var c = 1;
  var h = $m_s_util_hashing_MurmurHash3$().cc(this.be, this.bP);
  a = ((a + h) | 0);
  b = (b ^ h);
  c = Math.imul(c, (1 | h));
  h = $m_s_util_hashing_MurmurHash3$().cc(this.bf, this.bQ);
  a = ((a + h) | 0);
  b = (b ^ h);
  c = Math.imul(c, (1 | h));
  h = $m_s_util_hashing_MurmurHash3$().cc(this.bg, this.bR);
  a = ((a + h) | 0);
  b = (b ^ h);
  c = Math.imul(c, (1 | h));
  h = $m_s_util_hashing_MurmurHash3$().cc(this.bh, this.bS);
  a = ((a + h) | 0);
  b = (b ^ h);
  c = Math.imul(c, (1 | h));
  h = $m_s_util_hashing_MurmurHash3$().dx;
  h = $m_s_util_hashing_MurmurHash3$().w(h, a);
  h = $m_s_util_hashing_MurmurHash3$().w(h, b);
  h = $m_s_util_hashing_MurmurHash3$().cY(h, c);
  return $m_s_util_hashing_MurmurHash3$().ar(h, 4);
});
$p.cd = (function(key, value) {
  return this.eb(key, value);
});
function $isArrayOf_sci_Map$Map4(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.c9)));
}
var $d_sci_Map$Map4 = new $TypeData().i($c_sci_Map$Map4, "scala.collection.immutable.Map$Map4", ({
  c9: 1,
  ad: 1,
  a9: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  ab: 1,
  aa: 1,
  d: 1,
  a2: 1,
  r: 1,
  af: 1,
  a3: 1,
  k: 1,
  a: 1
}));
function $isArrayOf_sci_HashSet(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.fQ)));
}
/** @constructor */
function $c_scm_AbstractSet() {
}
$p = $c_scm_AbstractSet.prototype = new $h_sc_AbstractSet();
$p.constructor = $c_scm_AbstractSet;
/** @constructor */
function $h_scm_AbstractSet() {
}
$h_scm_AbstractSet.prototype = $p;
$p.b2 = (function() {
  return this;
});
function $ct_sci_LazyList__O__($thiz, lazyState) {
  $thiz.b8 = ((lazyState === $m_sci_LazyList$EmptyMarker$()) ? null : $m_sci_LazyList$Uninitialized$());
  $thiz.ch = ((lazyState === $m_sci_LazyList$EmptyMarker$()) ? null : lazyState);
  return $thiz;
}
function $ct_sci_LazyList__O__sci_LazyList__($thiz, head, tail) {
  $ct_sci_LazyList__O__($thiz, $m_sci_LazyList$EmptyMarker$());
  $thiz.b8 = head;
  $thiz.ch = tail;
  return $thiz;
}
function $p_sci_LazyList__initState__V($thiz) {
  if (($thiz.b8 === $m_sci_LazyList$Uninitialized$())) {
    if (($thiz.ch === $m_sci_LazyList$MidEvaluation$())) {
      throw $ct_jl_RuntimeException__T__(new $c_jl_RuntimeException(), "LazyList evaluation depends on its own result (self-reference); see docs for more info");
    }
    var fun = $thiz.ch;
    $thiz.ch = $m_sci_LazyList$MidEvaluation$();
    try {
      var l = $p_sci_LazyList__evaluated__sci_LazyList(fun.F());
    } finally {
      $thiz.ch = fun;
    }
    $thiz.ch = l.ch;
    $thiz.b8 = l.b8;
  }
}
function $p_sci_LazyList__evaluated__sci_LazyList($thiz) {
  while (true) {
    if (($thiz.b8 !== $m_sci_LazyList$Uninitialized$())) {
      return (($thiz.ch === null) ? $m_sci_LazyList$().a2 : $thiz);
    } else {
      $p_sci_LazyList__initState__V($thiz);
    }
  }
}
function $p_sci_LazyList__addStringNoForce__jl_StringBuilder__T__T__T__jl_StringBuilder($thiz, b, start, sep, end) {
  b.p = (("" + b.p) + start);
  if (($thiz.b8 === $m_sci_LazyList$Uninitialized$())) {
    b.p = (b.p + "<not computed>");
  } else if (($p_sci_LazyList__evaluated__sci_LazyList($thiz) !== $m_sci_LazyList$().a2)) {
    var obj = $thiz.n();
    b.p = (("" + b.p) + obj);
    var cursor = $thiz;
    var scout = $thiz.b3();
    if ((cursor !== scout)) {
      cursor = scout;
      var this$1 = scout;
      if (((this$1.b8 !== $m_sci_LazyList$Uninitialized$()) && ($p_sci_LazyList__evaluated__sci_LazyList(this$1) !== $m_sci_LazyList$().a2))) {
        scout = scout.b3();
        while (true) {
          if ((cursor !== scout)) {
            var this$2 = scout;
            var $x_1 = ((this$2.b8 !== $m_sci_LazyList$Uninitialized$()) && ($p_sci_LazyList__evaluated__sci_LazyList(this$2) !== $m_sci_LazyList$().a2));
          } else {
            var $x_1 = false;
          }
          if ($x_1) {
            var c = cursor;
            b.p = (("" + b.p) + sep);
            var obj$1 = c.n();
            b.p = (("" + b.p) + obj$1);
            cursor = cursor.b3();
            scout = scout.b3();
            var this$3 = scout;
            if (((this$3.b8 !== $m_sci_LazyList$Uninitialized$()) && ($p_sci_LazyList__evaluated__sci_LazyList(this$3) !== $m_sci_LazyList$().a2))) {
              scout = scout.b3();
            }
          } else {
            break;
          }
        }
      }
    }
    var this$4 = scout;
    if ((!((this$4.b8 !== $m_sci_LazyList$Uninitialized$()) && ($p_sci_LazyList__evaluated__sci_LazyList(this$4) !== $m_sci_LazyList$().a2)))) {
      while ((cursor !== scout)) {
        var c$1 = cursor;
        b.p = (("" + b.p) + sep);
        var obj$2 = c$1.n();
        b.p = (("" + b.p) + obj$2);
        cursor = cursor.b3();
      }
      if ((!(cursor.b8 !== $m_sci_LazyList$Uninitialized$()))) {
        b.p = (("" + b.p) + sep);
        b.p = (b.p + "<not computed>");
      }
    } else {
      if ((cursor !== $thiz)) {
        var runner = $thiz;
        while ((runner !== scout)) {
          runner = runner.b3();
          scout = scout.b3();
        }
        while (true) {
          var ct = cursor.b3();
          if ((ct !== scout)) {
            var c$2 = cursor;
            b.p = (("" + b.p) + sep);
            var obj$3 = c$2.n();
            b.p = (("" + b.p) + obj$3);
          }
          cursor = ct;
          if ((cursor !== scout)) {
          } else {
            break;
          }
        }
      }
      b.p = (("" + b.p) + sep);
      b.p = (b.p + "<cycle>");
    }
  }
  b.p = (("" + b.p) + end);
  return b;
}
/** @constructor */
function $c_sci_LazyList() {
  this.b8 = null;
  this.ch = null;
}
$p = $c_sci_LazyList.prototype = new $h_sci_AbstractSeq();
$p.constructor = $c_sci_LazyList;
/** @constructor */
function $h_sci_LazyList() {
}
$h_sci_LazyList.prototype = $p;
$p.q = (function() {
  return $f_sc_LinearSeqOps__length__I(this);
});
$p.bc = (function(len) {
  return $f_sc_LinearSeqOps__lengthCompare__I__I(this, len);
});
$p.jd = (function(x) {
  return $f_sc_LinearSeqOps__isDefinedAt__I__Z(this, x);
});
$p.v = (function(n) {
  return $f_sc_LinearSeqOps__apply__I__O(this, n);
});
$p.eW = (function(that) {
  return $f_sc_LinearSeqOps__sameElements__sc_IterableOnce__Z(this, that);
});
$p.bq = (function() {
  return "LinearSeq";
});
$p.c = (function() {
  return ($p_sci_LazyList__evaluated__sci_LazyList(this) === $m_sci_LazyList$().a2);
});
$p.x = (function() {
  return (((this.b8 !== $m_sci_LazyList$Uninitialized$()) && ($p_sci_LazyList__evaluated__sci_LazyList(this) === $m_sci_LazyList$().a2)) ? 0 : (-1));
});
$p.n = (function() {
  if (($p_sci_LazyList__evaluated__sci_LazyList(this) === $m_sci_LazyList$().a2)) {
    throw $ct_ju_NoSuchElementException__T__(new $c_ju_NoSuchElementException(), "head of empty lazy list");
  } else {
    return this.b8;
  }
});
$p.b3 = (function() {
  if (($p_sci_LazyList__evaluated__sci_LazyList(this) === $m_sci_LazyList$().a2)) {
    throw new $c_jl_UnsupportedOperationException("tail of empty lazy list");
  } else {
    return this.ch;
  }
});
$p.pZ = (function() {
  var these = this;
  var those = this;
  if ((!($p_sci_LazyList__evaluated__sci_LazyList(these) === $m_sci_LazyList$().a2))) {
    these = these.b3();
  }
  while ((those !== these)) {
    if (($p_sci_LazyList__evaluated__sci_LazyList(these) === $m_sci_LazyList$().a2)) {
      return this;
    }
    these = these.b3();
    if (($p_sci_LazyList__evaluated__sci_LazyList(these) === $m_sci_LazyList$().a2)) {
      return this;
    }
    these = these.b3();
    if ((these === those)) {
      return this;
    }
    those = those.b3();
  }
  return this;
});
$p.i = (function() {
  return (((this.b8 !== $m_sci_LazyList$Uninitialized$()) && ($p_sci_LazyList__evaluated__sci_LazyList(this) === $m_sci_LazyList$().a2)) ? $m_sc_Iterator$().O : new $c_sci_LazyList$LazyIterator(this));
});
$p.bm = (function(f) {
  var \u03b4this$tailLocal1 = this;
  while (true) {
    if ((!($p_sci_LazyList__evaluated__sci_LazyList(\u03b4this$tailLocal1) === $m_sci_LazyList$().a2))) {
      f.b(\u03b4this$tailLocal1.n());
      \u03b4this$tailLocal1 = \u03b4this$tailLocal1.b3();
    } else {
      return (void 0);
    }
  }
});
$p.bZ = (function() {
  return "LazyList";
});
$p.pP = (function(n) {
  return ((n <= 0) ? this : (((this.b8 !== $m_sci_LazyList$Uninitialized$()) && ($p_sci_LazyList__evaluated__sci_LazyList(this) === $m_sci_LazyList$().a2)) ? $m_sci_LazyList$().a2 : $m_sci_LazyList$().r8(this, n)));
});
$p.dy = (function(sb, start, sep, end) {
  this.pZ();
  $p_sci_LazyList__addStringNoForce__jl_StringBuilder__T__T__T__jl_StringBuilder(this, sb.aM, start, sep, end);
  return sb;
});
$p.t = (function() {
  return $p_sci_LazyList__addStringNoForce__jl_StringBuilder__T__T__T__jl_StringBuilder(this, $ct_jl_StringBuilder__T__(new $c_jl_StringBuilder(), "LazyList"), "(", ", ", ")").p;
});
$p.bn = (function() {
  return $m_sci_LazyList$();
});
$p.l = (function() {
  return this.b3();
});
$p.nm = (function(n) {
  return this.pP(n);
});
$p.ca = (function(x) {
  return $f_sc_LinearSeqOps__isDefinedAt__I__Z(this, (x | 0));
});
$p.b = (function(v1) {
  return $f_sc_LinearSeqOps__apply__I__O(this, (v1 | 0));
});
function $isArrayOf_sci_LazyList(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.c5)));
}
var $d_sci_LazyList = new $TypeData().i($c_sci_LazyList, "scala.collection.immutable.LazyList", ({
  c5: 1,
  x: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  r: 1,
  w: 1,
  v: 1,
  aK: 1,
  an: 1,
  aP: 1,
  aO: 1,
  a: 1
}));
function $isArrayOf_sci_WrappedString(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.gz)));
}
/** @constructor */
function $c_sjsr_WrappedVarArgs(array) {
  this.gQ = null;
  this.gQ = array;
}
$p = $c_sjsr_WrappedVarArgs.prototype = new $h_O();
$p.constructor = $c_sjsr_WrappedVarArgs;
/** @constructor */
function $h_sjsr_WrappedVarArgs() {
}
$h_sjsr_WrappedVarArgs.prototype = $p;
$p.cq = (function(f) {
  return $f_sci_StrictOptimizedSeqOps__distinctBy__F1__O(this, f);
});
$p.gZ = (function(that) {
  return $f_sci_IndexedSeq__canEqual__O__Z(this, that);
});
$p.eW = (function(o) {
  return $f_sci_IndexedSeq__sameElements__sc_IterableOnce__Z(this, o);
});
$p.gX = (function() {
  return $m_sci_IndexedSeqDefaults$().mf;
});
$p.i = (function() {
  return $ct_sc_IndexedSeqView$IndexedSeqViewIterator__sc_IndexedSeqView__(new $c_sc_IndexedSeqView$IndexedSeqViewIterator(), new $c_sc_IndexedSeqView$Id(this));
});
$p.bc = (function(len) {
  var x = this.q();
  return ((x === len) ? 0 : ((x < len) ? (-1) : 1));
});
$p.x = (function() {
  return this.q();
});
$p.k = (function(o) {
  return $f_sc_Seq__equals__O__Z(this, o);
});
$p.r = (function() {
  return $m_s_util_hashing_MurmurHash3$().ob(this);
});
$p.t = (function() {
  return $f_sc_Iterable__toString__T(this);
});
$p.c = (function() {
  return $f_sc_SeqOps__isEmpty__Z(this);
});
$p.bX = (function(x, default$1) {
  return $f_s_PartialFunction__applyOrElse__O__F1__O(this, x, default$1);
});
$p.g8 = (function() {
  return $m_sjsr_WrappedVarArgs$().aW();
});
$p.bm = (function(f) {
  $f_sc_IterableOnceOps__foreach__F1__V(this, f);
});
$p.bI = (function(dest, start, n) {
  return $f_sc_IterableOnceOps__copyToArray__O__I__I__I(this, dest, start, n);
});
$p.dy = (function(b, start, sep, end) {
  return $f_sc_IterableOnceOps__addString__scm_StringBuilder__T__T__T__scm_StringBuilder(this, b, start, sep, end);
});
$p.dD = (function() {
  return $m_sjsr_WrappedVarArgs$();
});
$p.q = (function() {
  return (this.gQ.length | 0);
});
$p.v = (function(idx) {
  return this.gQ[idx];
});
$p.bZ = (function() {
  return "WrappedVarArgs";
});
$p.g2 = (function(coll) {
  return $m_sjsr_WrappedVarArgs$().j4(coll);
});
$p.ca = (function(x) {
  return $f_sc_SeqOps__isDefinedAt__I__Z(this, (x | 0));
});
$p.b = (function(v1) {
  return this.v((v1 | 0));
});
function $isArrayOf_sjsr_WrappedVarArgs(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.cB)));
}
var $d_sjsr_WrappedVarArgs = new $TypeData().i($c_sjsr_WrappedVarArgs, "scala.scalajs.runtime.WrappedVarArgs", ({
  cB: 1,
  y: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  r: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  w: 1,
  v: 1,
  p: 1,
  o: 1,
  C: 1,
  z: 1,
  k: 1,
  q: 1,
  a: 1
}));
/** @constructor */
function $c_sci_HashMap(rootNode) {
  this.b7 = null;
  this.b7 = rootNode;
}
$p = $c_sci_HashMap.prototype = new $h_sci_AbstractMap();
$p.constructor = $c_sci_HashMap;
/** @constructor */
function $h_sci_HashMap() {
}
$h_sci_HashMap.prototype = $p;
$p.g6 = (function() {
  return $m_sci_HashMap$();
});
$p.x = (function() {
  return this.b7.aE;
});
$p.ax = (function() {
  return this.b7.aE;
});
$p.c = (function() {
  return (this.b7.aE === 0);
});
$p.i = (function() {
  return (this.c() ? $m_sc_Iterator$().O : new $c_sci_MapKeyValueTupleIterator(this.b7));
});
$p.bl = (function(key) {
  var keyUnimprovedHash = $m_sr_Statics$().C(key);
  var keyHash = $m_sc_Hashing$().c0(keyUnimprovedHash);
  return this.b7.iP(key, keyUnimprovedHash, keyHash, 0);
});
$p.b = (function(key) {
  var keyUnimprovedHash = $m_sr_Statics$().C(key);
  var keyHash = $m_sc_Hashing$().c0(keyUnimprovedHash);
  return this.b7.iH(key, keyUnimprovedHash, keyHash, 0);
});
$p.cr = (function(key) {
  var keyUnimprovedHash = $m_sr_Statics$().C(key);
  var keyHash = $m_sc_Hashing$().c0(keyUnimprovedHash);
  return this.b7.h7(key, keyUnimprovedHash, keyHash, 0);
});
$p.c9 = (function(key, default$1) {
  var keyUnimprovedHash = $m_sr_Statics$().C(key);
  var keyHash = $m_sc_Hashing$().c0(keyUnimprovedHash);
  return this.b7.j6(key, keyUnimprovedHash, keyHash, 0, default$1);
});
$p.eZ = (function(key, value) {
  var keyUnimprovedHash = $m_sr_Statics$().C(key);
  var newRootNode = this.b7.om(key, value, keyUnimprovedHash, $m_sc_Hashing$().c0(keyUnimprovedHash), 0, true);
  return ((newRootNode === this.b7) ? this : new $c_sci_HashMap(newRootNode));
});
$p.e1 = (function(f) {
  this.b7.e1(f);
});
$p.k = (function(that) {
  if ((that instanceof $c_sci_HashMap)) {
    if ((this === that)) {
      return true;
    } else {
      var x = this.b7;
      var x$2 = that.b7;
      return ((x === null) ? (x$2 === null) : x.k(x$2));
    }
  } else {
    return $f_sc_Map__equals__O__Z(this, that);
  }
});
$p.r = (function() {
  if (this.c()) {
    return $m_s_util_hashing_MurmurHash3$().iC;
  } else {
    var hashIterator = new $c_sci_MapKeyValueTupleHashIterator(this.b7);
    return $m_s_util_hashing_MurmurHash3$().jv(hashIterator, $m_s_util_hashing_MurmurHash3$().dx);
  }
});
$p.bZ = (function() {
  return "HashMap";
});
$p.cd = (function(key, value) {
  return this.eZ(key, value);
});
function $isArrayOf_sci_HashMap(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.c4)));
}
var $d_sci_HashMap = new $TypeData().i($c_sci_HashMap, "scala.collection.immutable.HashMap", ({
  c4: 1,
  ad: 1,
  a9: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  ab: 1,
  aa: 1,
  d: 1,
  a2: 1,
  r: 1,
  af: 1,
  a3: 1,
  k: 1,
  fD: 1,
  gm: 1,
  a: 1,
  U: 1
}));
function $isArrayOf_sci_TreeSeqMap(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.gn)));
}
function $isArrayOf_sci_VectorMap(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.gx)));
}
/** @constructor */
function $c_scm_AbstractBuffer() {
}
$p = $c_scm_AbstractBuffer.prototype = new $h_scm_AbstractSeq();
$p.constructor = $c_scm_AbstractBuffer;
/** @constructor */
function $h_scm_AbstractBuffer() {
}
$h_scm_AbstractBuffer.prototype = $p;
$p.aU = (function(elems) {
  return $f_scm_Growable__addAll__sc_IterableOnce__scm_Growable(this, elems);
});
function $ct_scm_HashSet__I__D__($thiz, initialCapacity, loadFactor) {
  $thiz.iv = loadFactor;
  $thiz.aK = new ($d_scm_HashSet$Node.r().C)($p_scm_HashSet__tableSizeFor__I__I($thiz, initialCapacity));
  $thiz.iw = $p_scm_HashSet__newThreshold__I__I($thiz, $thiz.aK.a.length);
  $thiz.dt = 0;
  return $thiz;
}
function $ct_scm_HashSet__($thiz) {
  $ct_scm_HashSet__I__D__($thiz, 16, 0.75);
  return $thiz;
}
function $p_scm_HashSet__improveHash__I__I($thiz, originalHash) {
  return (originalHash ^ ((originalHash >>> 16) | 0));
}
function $p_scm_HashSet__addElem__O__I__Z($thiz, elem, hash) {
  var idx = (hash & (($thiz.aK.a.length - 1) | 0));
  matchResult4: {
    var x10 = $thiz.aK.a[idx];
    if ((x10 === null)) {
      $thiz.aK.a[idx] = new $c_scm_HashSet$Node(elem, hash, null);
      break matchResult4;
    }
    var prev = null;
    var n = x10;
    while (((n !== null) && (n.cQ <= hash))) {
      if (((n.cQ === hash) && $m_sr_BoxesRunTime$().j(elem, n.eF))) {
        return false;
      }
      prev = n;
      n = n.aL;
    }
    if ((prev === null)) {
      $thiz.aK.a[idx] = new $c_scm_HashSet$Node(elem, hash, x10);
    } else {
      var this$3 = prev;
      var n$1 = new $c_scm_HashSet$Node(elem, hash, prev.aL);
      this$3.aL = n$1;
    }
  }
  $thiz.dt = ((1 + $thiz.dt) | 0);
  return true;
}
function $p_scm_HashSet__growTable__I__V($thiz, newlen) {
  var oldlen = $thiz.aK.a.length;
  $thiz.iw = $p_scm_HashSet__newThreshold__I__I($thiz, newlen);
  if (($thiz.dt === 0)) {
    $thiz.aK = new ($d_scm_HashSet$Node.r().C)(newlen);
  } else {
    $thiz.aK = $m_ju_Arrays$().S($thiz.aK, newlen);
    var preLow = new $c_scm_HashSet$Node(null, 0, null);
    var preHigh = new $c_scm_HashSet$Node(null, 0, null);
    while ((oldlen < newlen)) {
      var i = 0;
      while ((i < oldlen)) {
        var old = $thiz.aK.a[i];
        if ((old !== null)) {
          preLow.aL = null;
          preHigh.aL = null;
          var lastLow = preLow;
          var lastHigh = preHigh;
          var n = old;
          while ((n !== null)) {
            var next = n.aL;
            if (((n.cQ & oldlen) === 0)) {
              var this$2 = lastLow;
              var n$1 = n;
              this$2.aL = n$1;
              lastLow = n;
            } else {
              var this$3 = lastHigh;
              var n$2 = n;
              this$3.aL = n$2;
              lastHigh = n;
            }
            n = next;
          }
          var this$4 = lastLow;
          this$4.aL = null;
          if ((old !== preLow.aL)) {
            $thiz.aK.a[i] = preLow.aL;
          }
          if ((preHigh.aL !== null)) {
            $thiz.aK.a[((i + oldlen) | 0)] = preHigh.aL;
            var this$5 = lastHigh;
            this$5.aL = null;
          }
        }
        i = ((1 + i) | 0);
      }
      oldlen = (oldlen << 1);
    }
  }
}
function $p_scm_HashSet__tableSizeFor__I__I($thiz, capacity) {
  var x = ((capacity - 1) | 0);
  var i = ((x > 4) ? x : 4);
  var x$1 = ((((-2147483648) >> Math.clz32(i)) & i) << 1);
  return ((x$1 < 1073741824) ? x$1 : 1073741824);
}
function $p_scm_HashSet__newThreshold__I__I($thiz, size) {
  return $doubleToInt((size * $thiz.iv));
}
/** @constructor */
function $c_scm_HashSet() {
  this.iv = 0.0;
  this.aK = null;
  this.iw = 0;
  this.dt = 0;
}
$p = $c_scm_HashSet.prototype = new $h_scm_AbstractSet();
$p.constructor = $c_scm_HashSet;
/** @constructor */
function $h_scm_HashSet() {
}
$h_scm_HashSet.prototype = $p;
$p.ax = (function() {
  return this.dt;
});
$p.bl = (function(elem) {
  var hash = $p_scm_HashSet__improveHash__I__I(this, $m_sr_Statics$().C(elem));
  matchResult1: {
    var $x_1;
    var x1 = this.aK.a[(hash & ((this.aK.a.length - 1) | 0))];
    if ((x1 === null)) {
      var $x_1 = null;
      break matchResult1;
    }
    var $x_1 = x1.pX(elem, hash);
  }
  return ($x_1 !== null);
});
$p.aX = (function(size) {
  var target = $p_scm_HashSet__tableSizeFor__I__I(this, $doubleToInt((((1 + size) | 0) / this.iv)));
  if ((target > this.aK.a.length)) {
    $p_scm_HashSet__growTable__I__V(this, target);
  }
});
$p.gV = (function(elem) {
  if ((((1 + this.dt) | 0) >= this.iw)) {
    $p_scm_HashSet__growTable__I__V(this, (this.aK.a.length << 1));
  }
  return $p_scm_HashSet__addElem__O__I__Z(this, elem, $p_scm_HashSet__improveHash__I__I(this, $m_sr_Statics$().C(elem)));
});
$p.n1 = (function(xs) {
  $f_scm_Builder__sizeHint__sc_IterableOnce__I__V(this, xs, 0);
  if (false) {
    var f = new $c_sr_AbstractFunction2_$$Lambda$b4228bd32034ae3b2f0c5fc896319aa4b79b55f8(((v1$2, v2$2) => {
      $p_scm_HashSet__addElem__O__I__Z(this, v1$2, $p_scm_HashSet__improveHash__I__I(this, (v2$2 | 0)));
    }));
    xs.rK.rO(f);
    return this;
  } else if ((xs instanceof $c_scm_HashSet)) {
    var iter = new $c_scm_HashSet$$anon$2(xs);
    while (iter.m()) {
      var next = iter.g();
      $p_scm_HashSet__addElem__O__I__Z(this, next.eF, next.cQ);
    }
    return this;
  } else if (false) {
    var iter$2 = xs.pQ();
    while (iter$2.m()) {
      var next$2 = iter$2.g();
      $p_scm_HashSet__addElem__O__I__Z(this, next$2.nL(), next$2.nE());
    }
    return this;
  } else {
    return $f_scm_Growable__addAll__sc_IterableOnce__scm_Growable(this, xs);
  }
});
$p.i = (function() {
  return new $c_scm_HashSet$$anon$1(this);
});
$p.bn = (function() {
  return $m_scm_HashSet$();
});
$p.x = (function() {
  return this.dt;
});
$p.c = (function() {
  return (this.dt === 0);
});
$p.bZ = (function() {
  return "HashSet";
});
$p.r = (function() {
  var setIterator = new $c_scm_HashSet$$anon$1(this);
  var hashIterator = ((!setIterator.m()) ? setIterator : new $c_scm_HashSet$$anon$3(this));
  return $m_s_util_hashing_MurmurHash3$().jv(hashIterator, $m_s_util_hashing_MurmurHash3$().mT);
});
$p.aU = (function(elems) {
  return this.n1(elems);
});
$p.aV = (function(elem) {
  this.gV(elem);
  return this;
});
function $isArrayOf_scm_HashSet(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.cm)));
}
var $d_scm_HashSet = new $TypeData().i($c_scm_HashSet, "scala.collection.mutable.HashSet", ({
  cm: 1,
  gA: 1,
  fj: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  fB: 1,
  d: 1,
  aN: 1,
  J: 1,
  A: 1,
  H: 1,
  G: 1,
  I: 1,
  M: 1,
  au: 1,
  h0: 1,
  gZ: 1,
  k: 1,
  a: 1
}));
function $isArrayOf_sci_ListMap(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.g1)));
}
function $isArrayOf_scm_LinkedHashSet(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.gV)));
}
/** @constructor */
function $c_sci_ArraySeq() {
}
$p = $c_sci_ArraySeq.prototype = new $h_sci_AbstractSeq();
$p.constructor = $c_sci_ArraySeq;
/** @constructor */
function $h_sci_ArraySeq() {
}
$h_sci_ArraySeq.prototype = $p;
$p.bc = (function(len) {
  var x = this.q();
  return ((x === len) ? 0 : ((x < len) ? (-1) : 1));
});
$p.x = (function() {
  return this.q();
});
$p.bq = (function() {
  return "IndexedSeq";
});
$p.gZ = (function(that) {
  return $f_sci_IndexedSeq__canEqual__O__Z(this, that);
});
$p.eW = (function(o) {
  return $f_sci_IndexedSeq__sameElements__sc_IterableOnce__Z(this, o);
});
$p.cq = (function(f) {
  return $f_sci_StrictOptimizedSeqOps__distinctBy__F1__O(this, f);
});
$p.eR = (function(coll) {
  return $m_sci_ArraySeq$().j1(coll, this.a0());
});
$p.g8 = (function() {
  return $m_sci_ArraySeq$().hc(this.a0());
});
$p.dD = (function() {
  return $m_sci_ArraySeq$().ih;
});
$p.bZ = (function() {
  return "ArraySeq";
});
$p.bI = (function(xs, start, len) {
  var srcLen = this.q();
  var destLen = $m_jl_reflect_Array$().bJ(xs);
  var limit = ((len < srcLen) ? len : srcLen);
  var capacity = ((start < 0) ? destLen : ((destLen - start) | 0));
  var total = ((capacity < limit) ? capacity : limit);
  var copied = ((total < 0) ? 0 : total);
  if ((copied > 0)) {
    $m_s_Array$().fZ(this.cv(), 0, xs, start, copied);
  }
  return copied;
});
$p.gX = (function() {
  return 2147483647;
});
$p.bn = (function() {
  return $m_sci_ArraySeq$().ih;
});
$p.g2 = (function(coll) {
  return $m_sci_ArraySeq$().j1(coll, this.a0());
});
function $isArrayOf_sci_ArraySeq(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.V)));
}
function $ct_sci_Vector__AO__($thiz, prefix1) {
  $thiz.d = prefix1;
  return $thiz;
}
/** @constructor */
function $c_sci_Vector() {
  this.d = null;
}
$p = $c_sci_Vector.prototype = new $h_sci_AbstractSeq();
$p.constructor = $c_sci_Vector;
/** @constructor */
function $h_sci_Vector() {
}
$h_sci_Vector.prototype = $p;
$p.bc = (function(len) {
  var x = this.q();
  return ((x === len) ? 0 : ((x < len) ? (-1) : 1));
});
$p.x = (function() {
  return this.q();
});
$p.bq = (function() {
  return "IndexedSeq";
});
$p.gZ = (function(that) {
  return $f_sci_IndexedSeq__canEqual__O__Z(this, that);
});
$p.eW = (function(o) {
  return $f_sci_IndexedSeq__sameElements__sc_IterableOnce__Z(this, o);
});
$p.cq = (function(f) {
  return $f_sci_StrictOptimizedSeqOps__distinctBy__F1__O(this, f);
});
$p.dD = (function() {
  return $m_sci_Vector$();
});
$p.q = (function() {
  return ((this instanceof $c_sci_BigVector) ? this.h : this.d.a.length);
});
$p.i = (function() {
  return ((this === $m_sci_Vector0$()) ? $m_sci_Vector$().ml : new $c_sci_NewVectorIterator(this, this.q(), this.cx()));
});
$p.bZ = (function() {
  return "Vector";
});
$p.bI = (function(xs, start, len) {
  return this.i().bI(xs, start, len);
});
$p.gX = (function() {
  return $m_sci_Vector$().mk;
});
$p.aw = (function(index) {
  return $m_scg_CommonErrors$().ja(index, ((this.q() - 1) | 0));
});
$p.bm = (function(f) {
  var c = this.cx();
  var i = 0;
  while ((i < c)) {
    var $x_1 = $m_sci_VectorStatics$();
    var idx = i;
    var c$1 = (((c + ((c >>> 31) | 0)) | 0) >> 1);
    var a = ((idx - c$1) | 0);
    var sign = (a >> 31);
    $x_1.iZ(((((((1 + c$1) | 0) - (((a ^ sign) - sign) | 0)) | 0) - 1) | 0), this.cw(i), f);
    i = ((1 + i) | 0);
  }
});
$p.bn = (function() {
  return $m_sci_Vector$();
});
function $isArrayOf_sci_Vector(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.a6)));
}
/** @constructor */
function $c_scm_ArraySeq() {
}
$p = $c_scm_ArraySeq.prototype = new $h_scm_AbstractSeq();
$p.constructor = $c_scm_ArraySeq;
/** @constructor */
function $h_scm_ArraySeq() {
}
$h_scm_ArraySeq.prototype = $p;
$p.bc = (function(len) {
  var x = this.q();
  return ((x === len) ? 0 : ((x < len) ? (-1) : 1));
});
$p.x = (function() {
  return this.q();
});
$p.bq = (function() {
  return "IndexedSeq";
});
$p.cq = (function(f) {
  return $f_sc_StrictOptimizedSeqOps__distinctBy__F1__O(this, f);
});
$p.dD = (function() {
  return $m_scm_ArraySeq$().iu;
});
$p.nB = (function(coll) {
  var evidence$1 = this.a0();
  var capacity = 0;
  var size = 0;
  var jsElems = null;
  var elementClass = evidence$1.aC();
  capacity = 0;
  size = 0;
  var isCharArrayBuilder = (elementClass === $d_C.l());
  jsElems = [];
  coll.x();
  var it = coll.i();
  while (it.m()) {
    var elem = it.g();
    var unboxedElem = (isCharArrayBuilder ? $uC(elem) : ((elem === null) ? $m_scm_ArrayBuilder$().hk(elementClass) : elem));
    jsElems.push(unboxedElem);
  }
  return $m_scm_ArraySeq$().jf($m_scm_ArrayBuilder$().hj(((elementClass === $d_V.l()) ? $d_jl_Void.l() : (((elementClass === $d_sr_Null$.l()) || (elementClass === $d_sr_Nothing$.l())) ? $d_O.l() : elementClass)), jsElems));
});
$p.g8 = (function() {
  return $m_scm_ArraySeq$().hc(this.a0());
});
$p.bZ = (function() {
  return "ArraySeq";
});
$p.bI = (function(xs, start, len) {
  var srcLen = this.q();
  var destLen = $m_jl_reflect_Array$().bJ(xs);
  var limit = ((len < srcLen) ? len : srcLen);
  var capacity = ((start < 0) ? destLen : ((destLen - start) | 0));
  var total = ((capacity < limit) ? capacity : limit);
  var copied = ((total < 0) ? 0 : total);
  if ((copied > 0)) {
    $m_s_Array$().fZ(this.bY(), 0, xs, start, copied);
  }
  return copied;
});
$p.k = (function(other) {
  if ((other instanceof $c_scm_ArraySeq)) {
    if (($m_jl_reflect_Array$().bJ(this.bY()) !== $m_jl_reflect_Array$().bJ(other.bY()))) {
      return false;
    }
  }
  return $f_sc_Seq__equals__O__Z(this, other);
});
$p.bn = (function() {
  return $m_scm_ArraySeq$().iu;
});
$p.eR = (function(coll) {
  return this.nB(coll);
});
$p.g2 = (function(coll) {
  return this.nB(coll);
});
function $isArrayOf_scm_ArraySeq(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.W)));
}
/** @constructor */
function $c_sci_ArraySeq$ofBoolean(unsafeArray) {
  this.d5 = null;
  this.d5 = unsafeArray;
}
$p = $c_sci_ArraySeq$ofBoolean.prototype = new $h_sci_ArraySeq();
$p.constructor = $c_sci_ArraySeq$ofBoolean;
/** @constructor */
function $h_sci_ArraySeq$ofBoolean() {
}
$h_sci_ArraySeq$ofBoolean.prototype = $p;
$p.q = (function() {
  return this.d5.a.length;
});
$p.fX = (function(i) {
  return this.d5.a[i];
});
$p.r = (function() {
  var this$1 = $m_s_util_hashing_MurmurHash3$();
  return this$1.aB(this.d5, this$1.ac);
});
$p.k = (function(that) {
  return ((that instanceof $c_sci_ArraySeq$ofBoolean) ? $m_ju_Arrays$().ns(this.d5, that.d5) : $f_sc_Seq__equals__O__Z(this, that));
});
$p.i = (function() {
  return new $c_sc_ArrayOps$ArrayIterator(this.d5);
});
$p.cv = (function() {
  return this.d5;
});
$p.a0 = (function() {
  return $m_s_reflect_ManifestFactory$BooleanManifest$();
});
$p.v = (function(i) {
  return this.fX(i);
});
$p.b = (function(v1) {
  return this.fX((v1 | 0));
});
function $isArrayOf_sci_ArraySeq$ofBoolean(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.bR)));
}
var $d_sci_ArraySeq$ofBoolean = new $TypeData().i($c_sci_ArraySeq$ofBoolean, "scala.collection.immutable.ArraySeq$ofBoolean", ({
  bR: 1,
  V: 1,
  x: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  r: 1,
  w: 1,
  v: 1,
  p: 1,
  o: 1,
  C: 1,
  y: 1,
  k: 1,
  q: 1,
  z: 1,
  Z: 1,
  a: 1
}));
/** @constructor */
function $c_sci_ArraySeq$ofByte(unsafeArray) {
  this.d6 = null;
  this.d6 = unsafeArray;
}
$p = $c_sci_ArraySeq$ofByte.prototype = new $h_sci_ArraySeq();
$p.constructor = $c_sci_ArraySeq$ofByte;
/** @constructor */
function $h_sci_ArraySeq$ofByte() {
}
$h_sci_ArraySeq$ofByte.prototype = $p;
$p.q = (function() {
  return this.d6.a.length;
});
$p.fP = (function(i) {
  return this.d6.a[i];
});
$p.r = (function() {
  var this$1 = $m_s_util_hashing_MurmurHash3$();
  return this$1.aB(this.d6, this$1.ac);
});
$p.k = (function(that) {
  return ((that instanceof $c_sci_ArraySeq$ofByte) ? $m_ju_Arrays$().no(this.d6, that.d6) : $f_sc_Seq__equals__O__Z(this, that));
});
$p.i = (function() {
  return new $c_sc_ArrayOps$ArrayIterator(this.d6);
});
$p.cv = (function() {
  return this.d6;
});
$p.a0 = (function() {
  return $m_s_reflect_ManifestFactory$ByteManifest$();
});
$p.v = (function(i) {
  return this.fP(i);
});
$p.b = (function(v1) {
  return this.fP((v1 | 0));
});
function $isArrayOf_sci_ArraySeq$ofByte(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.bS)));
}
var $d_sci_ArraySeq$ofByte = new $TypeData().i($c_sci_ArraySeq$ofByte, "scala.collection.immutable.ArraySeq$ofByte", ({
  bS: 1,
  V: 1,
  x: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  r: 1,
  w: 1,
  v: 1,
  p: 1,
  o: 1,
  C: 1,
  y: 1,
  k: 1,
  q: 1,
  z: 1,
  Z: 1,
  a: 1
}));
/** @constructor */
function $c_sci_ArraySeq$ofChar(unsafeArray) {
  this.cG = null;
  this.cG = unsafeArray;
}
$p = $c_sci_ArraySeq$ofChar.prototype = new $h_sci_ArraySeq();
$p.constructor = $c_sci_ArraySeq$ofChar;
/** @constructor */
function $h_sci_ArraySeq$ofChar() {
}
$h_sci_ArraySeq$ofChar.prototype = $p;
$p.q = (function() {
  return this.cG.a.length;
});
$p.fQ = (function(i) {
  return this.cG.a[i];
});
$p.r = (function() {
  var this$1 = $m_s_util_hashing_MurmurHash3$();
  return this$1.aB(this.cG, this$1.ac);
});
$p.k = (function(that) {
  return ((that instanceof $c_sci_ArraySeq$ofChar) ? $m_ju_Arrays$().np(this.cG, that.cG) : $f_sc_Seq__equals__O__Z(this, that));
});
$p.i = (function() {
  return new $c_sc_ArrayOps$ArrayIterator(this.cG);
});
$p.dy = (function(sb, start, sep, end) {
  return new $c_scm_ArraySeq$ofChar(this.cG).dy(sb, start, sep, end);
});
$p.cv = (function() {
  return this.cG;
});
$p.a0 = (function() {
  return $m_s_reflect_ManifestFactory$CharManifest$();
});
$p.v = (function(i) {
  return $bC(this.fQ(i));
});
$p.b = (function(v1) {
  return $bC(this.fQ((v1 | 0)));
});
function $isArrayOf_sci_ArraySeq$ofChar(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.bT)));
}
var $d_sci_ArraySeq$ofChar = new $TypeData().i($c_sci_ArraySeq$ofChar, "scala.collection.immutable.ArraySeq$ofChar", ({
  bT: 1,
  V: 1,
  x: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  r: 1,
  w: 1,
  v: 1,
  p: 1,
  o: 1,
  C: 1,
  y: 1,
  k: 1,
  q: 1,
  z: 1,
  Z: 1,
  a: 1
}));
/** @constructor */
function $c_sci_ArraySeq$ofDouble(unsafeArray) {
  this.d7 = null;
  this.d7 = unsafeArray;
}
$p = $c_sci_ArraySeq$ofDouble.prototype = new $h_sci_ArraySeq();
$p.constructor = $c_sci_ArraySeq$ofDouble;
/** @constructor */
function $h_sci_ArraySeq$ofDouble() {
}
$h_sci_ArraySeq$ofDouble.prototype = $p;
$p.q = (function() {
  return this.d7.a.length;
});
$p.fR = (function(i) {
  return this.d7.a[i];
});
$p.r = (function() {
  var this$1 = $m_s_util_hashing_MurmurHash3$();
  return this$1.aB(this.d7, this$1.ac);
});
$p.k = (function(that) {
  if ((that instanceof $c_sci_ArraySeq$ofDouble)) {
    var array = this.d7;
    var thatArray = that.d7;
    if ((array === thatArray)) {
      return true;
    } else if ((array.a.length === thatArray.a.length)) {
      var i = 0;
      while (((i < array.a.length) && (array.a[i] === thatArray.a[i]))) {
        i = ((1 + i) | 0);
      }
      return (i >= array.a.length);
    } else {
      return false;
    }
  } else {
    return $f_sc_Seq__equals__O__Z(this, that);
  }
});
$p.i = (function() {
  return new $c_sc_ArrayOps$ArrayIterator(this.d7);
});
$p.cv = (function() {
  return this.d7;
});
$p.a0 = (function() {
  return $m_s_reflect_ManifestFactory$DoubleManifest$();
});
$p.v = (function(i) {
  return this.fR(i);
});
$p.b = (function(v1) {
  return this.fR((v1 | 0));
});
function $isArrayOf_sci_ArraySeq$ofDouble(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.bU)));
}
var $d_sci_ArraySeq$ofDouble = new $TypeData().i($c_sci_ArraySeq$ofDouble, "scala.collection.immutable.ArraySeq$ofDouble", ({
  bU: 1,
  V: 1,
  x: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  r: 1,
  w: 1,
  v: 1,
  p: 1,
  o: 1,
  C: 1,
  y: 1,
  k: 1,
  q: 1,
  z: 1,
  Z: 1,
  a: 1
}));
/** @constructor */
function $c_sci_ArraySeq$ofFloat(unsafeArray) {
  this.d8 = null;
  this.d8 = unsafeArray;
}
$p = $c_sci_ArraySeq$ofFloat.prototype = new $h_sci_ArraySeq();
$p.constructor = $c_sci_ArraySeq$ofFloat;
/** @constructor */
function $h_sci_ArraySeq$ofFloat() {
}
$h_sci_ArraySeq$ofFloat.prototype = $p;
$p.q = (function() {
  return this.d8.a.length;
});
$p.fS = (function(i) {
  return this.d8.a[i];
});
$p.r = (function() {
  var this$1 = $m_s_util_hashing_MurmurHash3$();
  return this$1.aB(this.d8, this$1.ac);
});
$p.k = (function(that) {
  if ((that instanceof $c_sci_ArraySeq$ofFloat)) {
    var array = this.d8;
    var thatArray = that.d8;
    if ((array === thatArray)) {
      return true;
    } else if ((array.a.length === thatArray.a.length)) {
      var i = 0;
      while (((i < array.a.length) && (array.a[i] === thatArray.a[i]))) {
        i = ((1 + i) | 0);
      }
      return (i >= array.a.length);
    } else {
      return false;
    }
  } else {
    return $f_sc_Seq__equals__O__Z(this, that);
  }
});
$p.i = (function() {
  return new $c_sc_ArrayOps$ArrayIterator(this.d8);
});
$p.cv = (function() {
  return this.d8;
});
$p.a0 = (function() {
  return $m_s_reflect_ManifestFactory$FloatManifest$();
});
$p.v = (function(i) {
  return this.fS(i);
});
$p.b = (function(v1) {
  return this.fS((v1 | 0));
});
function $isArrayOf_sci_ArraySeq$ofFloat(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.bV)));
}
var $d_sci_ArraySeq$ofFloat = new $TypeData().i($c_sci_ArraySeq$ofFloat, "scala.collection.immutable.ArraySeq$ofFloat", ({
  bV: 1,
  V: 1,
  x: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  r: 1,
  w: 1,
  v: 1,
  p: 1,
  o: 1,
  C: 1,
  y: 1,
  k: 1,
  q: 1,
  z: 1,
  Z: 1,
  a: 1
}));
/** @constructor */
function $c_sci_ArraySeq$ofInt(unsafeArray) {
  this.d9 = null;
  this.d9 = unsafeArray;
}
$p = $c_sci_ArraySeq$ofInt.prototype = new $h_sci_ArraySeq();
$p.constructor = $c_sci_ArraySeq$ofInt;
/** @constructor */
function $h_sci_ArraySeq$ofInt() {
}
$h_sci_ArraySeq$ofInt.prototype = $p;
$p.q = (function() {
  return this.d9.a.length;
});
$p.fT = (function(i) {
  return this.d9.a[i];
});
$p.r = (function() {
  var this$1 = $m_s_util_hashing_MurmurHash3$();
  return this$1.aB(this.d9, this$1.ac);
});
$p.k = (function(that) {
  return ((that instanceof $c_sci_ArraySeq$ofInt) ? $m_ju_Arrays$().iU(this.d9, that.d9) : $f_sc_Seq__equals__O__Z(this, that));
});
$p.i = (function() {
  return new $c_sc_ArrayOps$ArrayIterator(this.d9);
});
$p.cv = (function() {
  return this.d9;
});
$p.a0 = (function() {
  return $m_s_reflect_ManifestFactory$IntManifest$();
});
$p.v = (function(i) {
  return this.fT(i);
});
$p.b = (function(v1) {
  return this.fT((v1 | 0));
});
function $isArrayOf_sci_ArraySeq$ofInt(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.bW)));
}
var $d_sci_ArraySeq$ofInt = new $TypeData().i($c_sci_ArraySeq$ofInt, "scala.collection.immutable.ArraySeq$ofInt", ({
  bW: 1,
  V: 1,
  x: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  r: 1,
  w: 1,
  v: 1,
  p: 1,
  o: 1,
  C: 1,
  y: 1,
  k: 1,
  q: 1,
  z: 1,
  Z: 1,
  a: 1
}));
/** @constructor */
function $c_sci_ArraySeq$ofLong(unsafeArray) {
  this.da = null;
  this.da = unsafeArray;
}
$p = $c_sci_ArraySeq$ofLong.prototype = new $h_sci_ArraySeq();
$p.constructor = $c_sci_ArraySeq$ofLong;
/** @constructor */
function $h_sci_ArraySeq$ofLong() {
}
$h_sci_ArraySeq$ofLong.prototype = $p;
$p.q = (function() {
  return ((this.da.a.length >>> 1) | 0);
});
$p.fU = (function(i) {
  var $x_1 = this.da.a;
  var $x_2 = (i << 1);
  return $bL($x_1[$x_2], $x_1[(($x_2 + 1) | 0)]);
});
$p.r = (function() {
  var this$1 = $m_s_util_hashing_MurmurHash3$();
  return this$1.aB(this.da, this$1.ac);
});
$p.k = (function(that) {
  return ((that instanceof $c_sci_ArraySeq$ofLong) ? $m_ju_Arrays$().nq(this.da, that.da) : $f_sc_Seq__equals__O__Z(this, that));
});
$p.i = (function() {
  return new $c_sc_ArrayOps$ArrayIterator(this.da);
});
$p.cv = (function() {
  return this.da;
});
$p.a0 = (function() {
  return $m_s_reflect_ManifestFactory$LongManifest$();
});
$p.v = (function(i) {
  return this.fU(i);
});
$p.b = (function(v1) {
  return this.fU((v1 | 0));
});
function $isArrayOf_sci_ArraySeq$ofLong(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.bX)));
}
var $d_sci_ArraySeq$ofLong = new $TypeData().i($c_sci_ArraySeq$ofLong, "scala.collection.immutable.ArraySeq$ofLong", ({
  bX: 1,
  V: 1,
  x: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  r: 1,
  w: 1,
  v: 1,
  p: 1,
  o: 1,
  C: 1,
  y: 1,
  k: 1,
  q: 1,
  z: 1,
  Z: 1,
  a: 1
}));
/** @constructor */
function $c_sci_ArraySeq$ofRef(unsafeArray) {
  this.cf = null;
  this.cf = unsafeArray;
}
$p = $c_sci_ArraySeq$ofRef.prototype = new $h_sci_ArraySeq();
$p.constructor = $c_sci_ArraySeq$ofRef;
/** @constructor */
function $h_sci_ArraySeq$ofRef() {
}
$h_sci_ArraySeq$ofRef.prototype = $p;
$p.a0 = (function() {
  return $m_s_reflect_ClassTag$().n8($objectGetClass(this.cf).ah.Q());
});
$p.q = (function() {
  return this.cf.a.length;
});
$p.v = (function(i) {
  return this.cf.a[i];
});
$p.r = (function() {
  var this$1 = $m_s_util_hashing_MurmurHash3$();
  return this$1.aB(this.cf, this$1.ac);
});
$p.k = (function(that) {
  return ((that instanceof $c_sci_ArraySeq$ofRef) ? $m_s_Array$().nt(this.cf, that.cf) : $f_sc_Seq__equals__O__Z(this, that));
});
$p.i = (function() {
  return new $c_sc_ArrayOps$ArrayIterator(this.cf);
});
$p.cv = (function() {
  return this.cf;
});
$p.b = (function(v1) {
  return this.v((v1 | 0));
});
function $isArrayOf_sci_ArraySeq$ofRef(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.bY)));
}
var $d_sci_ArraySeq$ofRef = new $TypeData().i($c_sci_ArraySeq$ofRef, "scala.collection.immutable.ArraySeq$ofRef", ({
  bY: 1,
  V: 1,
  x: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  r: 1,
  w: 1,
  v: 1,
  p: 1,
  o: 1,
  C: 1,
  y: 1,
  k: 1,
  q: 1,
  z: 1,
  Z: 1,
  a: 1
}));
/** @constructor */
function $c_sci_ArraySeq$ofShort(unsafeArray) {
  this.db = null;
  this.db = unsafeArray;
}
$p = $c_sci_ArraySeq$ofShort.prototype = new $h_sci_ArraySeq();
$p.constructor = $c_sci_ArraySeq$ofShort;
/** @constructor */
function $h_sci_ArraySeq$ofShort() {
}
$h_sci_ArraySeq$ofShort.prototype = $p;
$p.q = (function() {
  return this.db.a.length;
});
$p.fV = (function(i) {
  return this.db.a[i];
});
$p.r = (function() {
  var this$1 = $m_s_util_hashing_MurmurHash3$();
  return this$1.aB(this.db, this$1.ac);
});
$p.k = (function(that) {
  return ((that instanceof $c_sci_ArraySeq$ofShort) ? $m_ju_Arrays$().nr(this.db, that.db) : $f_sc_Seq__equals__O__Z(this, that));
});
$p.i = (function() {
  return new $c_sc_ArrayOps$ArrayIterator(this.db);
});
$p.cv = (function() {
  return this.db;
});
$p.a0 = (function() {
  return $m_s_reflect_ManifestFactory$ShortManifest$();
});
$p.v = (function(i) {
  return this.fV(i);
});
$p.b = (function(v1) {
  return this.fV((v1 | 0));
});
function $isArrayOf_sci_ArraySeq$ofShort(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.bZ)));
}
var $d_sci_ArraySeq$ofShort = new $TypeData().i($c_sci_ArraySeq$ofShort, "scala.collection.immutable.ArraySeq$ofShort", ({
  bZ: 1,
  V: 1,
  x: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  r: 1,
  w: 1,
  v: 1,
  p: 1,
  o: 1,
  C: 1,
  y: 1,
  k: 1,
  q: 1,
  z: 1,
  Z: 1,
  a: 1
}));
/** @constructor */
function $c_sci_ArraySeq$ofUnit(unsafeArray) {
  this.dS = null;
  this.dS = unsafeArray;
}
$p = $c_sci_ArraySeq$ofUnit.prototype = new $h_sci_ArraySeq();
$p.constructor = $c_sci_ArraySeq$ofUnit;
/** @constructor */
function $h_sci_ArraySeq$ofUnit() {
}
$h_sci_ArraySeq$ofUnit.prototype = $p;
$p.q = (function() {
  return this.dS.a.length;
});
$p.fW = (function(i) {
});
$p.r = (function() {
  var this$1 = $m_s_util_hashing_MurmurHash3$();
  return this$1.aB(this.dS, this$1.ac);
});
$p.k = (function(that) {
  return ((that instanceof $c_sci_ArraySeq$ofUnit) ? (this.dS.a.length === that.dS.a.length) : $f_sc_Seq__equals__O__Z(this, that));
});
$p.i = (function() {
  return new $c_sc_ArrayOps$ArrayIterator(this.dS);
});
$p.cv = (function() {
  return this.dS;
});
$p.a0 = (function() {
  return $m_s_reflect_ManifestFactory$UnitManifest$();
});
$p.v = (function(i) {
  this.fW(i);
});
$p.b = (function(v1) {
  this.fW((v1 | 0));
});
function $isArrayOf_sci_ArraySeq$ofUnit(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.c0)));
}
var $d_sci_ArraySeq$ofUnit = new $TypeData().i($c_sci_ArraySeq$ofUnit, "scala.collection.immutable.ArraySeq$ofUnit", ({
  c0: 1,
  V: 1,
  x: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  r: 1,
  w: 1,
  v: 1,
  p: 1,
  o: 1,
  C: 1,
  y: 1,
  k: 1,
  q: 1,
  z: 1,
  Z: 1,
  a: 1
}));
function $p_sci_List__loop$2__I__I__sci_List__I($thiz, len$1, i, xs) {
  var xs$tailLocal1 = xs;
  var i$tailLocal1 = i;
  while (true) {
    if ((i$tailLocal1 === len$1)) {
      return ((!xs$tailLocal1.c()) | 0);
    } else {
      if ((!xs$tailLocal1.c())) {
        var i$tailLocal1$tmp1 = ((1 + i$tailLocal1) | 0);
        var xs$tailLocal1$tmp1 = xs$tailLocal1.l();
        i$tailLocal1 = i$tailLocal1$tmp1;
        xs$tailLocal1 = xs$tailLocal1$tmp1;
        continue;
      }
      return (-1);
    }
  }
}
function $p_sci_List__listEq$1__sci_List__sci_List__Z($thiz, a, b) {
  var b$tailLocal1 = b;
  var a$tailLocal1 = a;
  while (true) {
    if ((a$tailLocal1 === b$tailLocal1)) {
      return true;
    } else {
      var aEmpty = a$tailLocal1.c();
      var bEmpty = b$tailLocal1.c();
      if (((!(aEmpty || bEmpty)) && $m_sr_BoxesRunTime$().j(a$tailLocal1.n(), b$tailLocal1.n()))) {
        var a$tailLocal1$tmp1 = a$tailLocal1.l();
        var b$tailLocal1$tmp1 = b$tailLocal1.l();
        a$tailLocal1 = a$tailLocal1$tmp1;
        b$tailLocal1 = b$tailLocal1$tmp1;
        continue;
      }
      return (aEmpty && bEmpty);
    }
  }
}
/** @constructor */
function $c_sci_List() {
}
$p = $c_sci_List.prototype = new $h_sci_AbstractSeq();
$p.constructor = $c_sci_List;
/** @constructor */
function $h_sci_List() {
}
$h_sci_List.prototype = $p;
$p.jd = (function(x) {
  return $f_sc_LinearSeqOps__isDefinedAt__I__Z(this, x);
});
$p.v = (function(n) {
  return $f_sc_LinearSeqOps__apply__I__O(this, n);
});
$p.eW = (function(that) {
  return $f_sc_LinearSeqOps__sameElements__sc_IterableOnce__Z(this, that);
});
$p.bq = (function() {
  return "LinearSeq";
});
$p.i = (function() {
  return new $c_sc_StrictOptimizedLinearSeqOps$$anon$1(this);
});
$p.cq = (function(f) {
  return $f_sci_StrictOptimizedSeqOps__distinctBy__F1__O(this, f);
});
$p.dD = (function() {
  return $m_sci_List$();
});
$p.mU = (function(prefix) {
  if (this.c()) {
    return prefix;
  } else if (prefix.c()) {
    return this;
  } else {
    var result = new $c_sci_$colon$colon(prefix.n(), this);
    var curr = result;
    var that = prefix.l();
    while ((!that.c())) {
      var temp = new $c_sci_$colon$colon(that.n(), this);
      curr.J = temp;
      curr = temp;
      that = that.l();
    }
    return result;
  }
});
$p.c = (function() {
  return (this === $m_sci_Nil$());
});
$p.eU = (function(prefix) {
  if ((prefix instanceof $c_sci_List)) {
    return this.mU(prefix);
  }
  if ((prefix.x() === 0)) {
    return this;
  }
  if ((prefix instanceof $c_scm_ListBuffer)) {
    if (this.c()) {
      return prefix.oh();
    }
  }
  var iter = prefix.i();
  if (iter.m()) {
    var result = new $c_sci_$colon$colon(iter.g(), this);
    var curr = result;
    while (iter.m()) {
      var temp = new $c_sci_$colon$colon(iter.g(), this);
      curr.J = temp;
      curr = temp;
    }
    return result;
  } else {
    return this;
  }
});
$p.n6 = (function(suffix) {
  return ((suffix instanceof $c_sci_List) ? suffix.mU(this) : $f_sc_StrictOptimizedSeqOps__appendedAll__sc_IterableOnce__O(this, suffix));
});
$p.rt = (function(n) {
  if ((this.c() || (n <= 0))) {
    var $x_1 = $m_sci_Nil$();
  } else {
    var h = new $c_sci_$colon$colon(this.n(), $m_sci_Nil$());
    var t = h;
    var rest = this.l();
    var i = 1;
    while (true) {
      if (rest.c()) {
        return this;
      }
      if ((i < n)) {
        i = ((1 + i) | 0);
        var nx = new $c_sci_$colon$colon(rest.n(), $m_sci_Nil$());
        t.J = nx;
        t = nx;
        rest = rest.l();
      } else {
        break;
      }
    }
    var $x_1 = h;
  }
  return $x_1;
});
$p.bm = (function(f) {
  var these = this;
  while ((!these.c())) {
    f.b(these.n());
    these = these.l();
  }
});
$p.q = (function() {
  var these = this;
  var len = 0;
  while ((!these.c())) {
    len = ((1 + len) | 0);
    these = these.l();
  }
  return len;
});
$p.bc = (function(len) {
  return ((len < 0) ? 1 : $p_sci_List__loop$2__I__I__sci_List__I(this, len, 0, this));
});
$p.bl = (function(elem) {
  var these = this;
  while ((!these.c())) {
    if ($m_sr_BoxesRunTime$().j(these.n(), elem)) {
      return true;
    }
    these = these.l();
  }
  return false;
});
$p.bZ = (function() {
  return "List";
});
$p.k = (function(o) {
  return ((o instanceof $c_sci_List) ? $p_sci_List__listEq$1__sci_List__sci_List__Z(this, this, o) : $f_sc_Seq__equals__O__Z(this, o));
});
$p.bn = (function() {
  return $m_sci_List$();
});
$p.nm = (function(n) {
  return $p_sc_StrictOptimizedLinearSeqOps__loop$2__I__sc_LinearSeq__sc_LinearSeq(this, n, this);
});
$p.ca = (function(x) {
  return $f_sc_LinearSeqOps__isDefinedAt__I__Z(this, (x | 0));
});
$p.b = (function(v1) {
  return $f_sc_LinearSeqOps__apply__I__O(this, (v1 | 0));
});
function $isArrayOf_sci_List(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.aQ)));
}
/** @constructor */
function $c_sci_VectorImpl() {
  this.d = null;
}
$p = $c_sci_VectorImpl.prototype = new $h_sci_Vector();
$p.constructor = $c_sci_VectorImpl;
/** @constructor */
function $h_sci_VectorImpl() {
}
$h_sci_VectorImpl.prototype = $p;
/** @constructor */
function $c_scm_ArraySeq$ofBoolean(array) {
  this.dm = null;
  this.dm = array;
}
$p = $c_scm_ArraySeq$ofBoolean.prototype = new $h_scm_ArraySeq();
$p.constructor = $c_scm_ArraySeq$ofBoolean;
/** @constructor */
function $h_scm_ArraySeq$ofBoolean() {
}
$h_scm_ArraySeq$ofBoolean.prototype = $p;
$p.q = (function() {
  return this.dm.a.length;
});
$p.fX = (function(index) {
  return this.dm.a[index];
});
$p.r = (function() {
  var this$1 = $m_s_util_hashing_MurmurHash3$();
  return this$1.aB(this.dm, this$1.ac);
});
$p.k = (function(that) {
  return ((that instanceof $c_scm_ArraySeq$ofBoolean) ? $m_ju_Arrays$().ns(this.dm, that.dm) : $c_scm_ArraySeq.prototype.k.call(this, that));
});
$p.i = (function() {
  return new $c_sc_ArrayOps$ArrayIterator(this.dm);
});
$p.bY = (function() {
  return this.dm;
});
$p.a0 = (function() {
  return $m_s_reflect_ManifestFactory$BooleanManifest$();
});
$p.v = (function(i) {
  return this.fX(i);
});
$p.b = (function(v1) {
  return this.fX((v1 | 0));
});
function $isArrayOf_scm_ArraySeq$ofBoolean(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.cc)));
}
var $d_scm_ArraySeq$ofBoolean = new $TypeData().i($c_scm_ArraySeq$ofBoolean, "scala.collection.mutable.ArraySeq$ofBoolean", ({
  cc: 1,
  W: 1,
  L: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  J: 1,
  A: 1,
  H: 1,
  O: 1,
  N: 1,
  p: 1,
  o: 1,
  S: 1,
  R: 1,
  k: 1,
  q: 1,
  a: 1
}));
/** @constructor */
function $c_scm_ArraySeq$ofByte(array) {
  this.dn = null;
  this.dn = array;
}
$p = $c_scm_ArraySeq$ofByte.prototype = new $h_scm_ArraySeq();
$p.constructor = $c_scm_ArraySeq$ofByte;
/** @constructor */
function $h_scm_ArraySeq$ofByte() {
}
$h_scm_ArraySeq$ofByte.prototype = $p;
$p.q = (function() {
  return this.dn.a.length;
});
$p.fP = (function(index) {
  return this.dn.a[index];
});
$p.r = (function() {
  var this$1 = $m_s_util_hashing_MurmurHash3$();
  return this$1.aB(this.dn, this$1.ac);
});
$p.k = (function(that) {
  return ((that instanceof $c_scm_ArraySeq$ofByte) ? $m_ju_Arrays$().no(this.dn, that.dn) : $c_scm_ArraySeq.prototype.k.call(this, that));
});
$p.i = (function() {
  return new $c_sc_ArrayOps$ArrayIterator(this.dn);
});
$p.bY = (function() {
  return this.dn;
});
$p.a0 = (function() {
  return $m_s_reflect_ManifestFactory$ByteManifest$();
});
$p.v = (function(i) {
  return this.fP(i);
});
$p.b = (function(v1) {
  return this.fP((v1 | 0));
});
function $isArrayOf_scm_ArraySeq$ofByte(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.cd)));
}
var $d_scm_ArraySeq$ofByte = new $TypeData().i($c_scm_ArraySeq$ofByte, "scala.collection.mutable.ArraySeq$ofByte", ({
  cd: 1,
  W: 1,
  L: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  J: 1,
  A: 1,
  H: 1,
  O: 1,
  N: 1,
  p: 1,
  o: 1,
  S: 1,
  R: 1,
  k: 1,
  q: 1,
  a: 1
}));
/** @constructor */
function $c_scm_ArraySeq$ofChar(array) {
  this.bH = null;
  this.bH = array;
}
$p = $c_scm_ArraySeq$ofChar.prototype = new $h_scm_ArraySeq();
$p.constructor = $c_scm_ArraySeq$ofChar;
/** @constructor */
function $h_scm_ArraySeq$ofChar() {
}
$h_scm_ArraySeq$ofChar.prototype = $p;
$p.q = (function() {
  return this.bH.a.length;
});
$p.fQ = (function(index) {
  return this.bH.a[index];
});
$p.r = (function() {
  var this$1 = $m_s_util_hashing_MurmurHash3$();
  return this$1.aB(this.bH, this$1.ac);
});
$p.k = (function(that) {
  return ((that instanceof $c_scm_ArraySeq$ofChar) ? $m_ju_Arrays$().np(this.bH, that.bH) : $c_scm_ArraySeq.prototype.k.call(this, that));
});
$p.i = (function() {
  return new $c_sc_ArrayOps$ArrayIterator(this.bH);
});
$p.dy = (function(sb, start, sep, end) {
  var jsb = sb.aM;
  if ((start.length !== 0)) {
    jsb.p = (("" + jsb.p) + start);
  }
  var len = this.bH.a.length;
  if ((len !== 0)) {
    if ((sep === "")) {
      jsb.n4(this.bH);
    } else {
      jsb.q();
      var c = this.bH.a[0];
      var str = ("" + $cToS(c));
      jsb.p = (jsb.p + str);
      var i = 1;
      while ((i < len)) {
        jsb.p = (("" + jsb.p) + sep);
        var c$1 = this.bH.a[i];
        var str$1 = ("" + $cToS(c$1));
        jsb.p = (jsb.p + str$1);
        i = ((1 + i) | 0);
      }
    }
  }
  if ((end.length !== 0)) {
    jsb.p = (("" + jsb.p) + end);
  }
  return sb;
});
$p.bY = (function() {
  return this.bH;
});
$p.a0 = (function() {
  return $m_s_reflect_ManifestFactory$CharManifest$();
});
$p.v = (function(i) {
  return $bC(this.fQ(i));
});
$p.b = (function(v1) {
  return $bC(this.fQ((v1 | 0)));
});
function $isArrayOf_scm_ArraySeq$ofChar(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.ce)));
}
var $d_scm_ArraySeq$ofChar = new $TypeData().i($c_scm_ArraySeq$ofChar, "scala.collection.mutable.ArraySeq$ofChar", ({
  ce: 1,
  W: 1,
  L: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  J: 1,
  A: 1,
  H: 1,
  O: 1,
  N: 1,
  p: 1,
  o: 1,
  S: 1,
  R: 1,
  k: 1,
  q: 1,
  a: 1
}));
/** @constructor */
function $c_scm_ArraySeq$ofDouble(array) {
  this.bT = null;
  this.bT = array;
}
$p = $c_scm_ArraySeq$ofDouble.prototype = new $h_scm_ArraySeq();
$p.constructor = $c_scm_ArraySeq$ofDouble;
/** @constructor */
function $h_scm_ArraySeq$ofDouble() {
}
$h_scm_ArraySeq$ofDouble.prototype = $p;
$p.q = (function() {
  return this.bT.a.length;
});
$p.fR = (function(index) {
  return this.bT.a[index];
});
$p.r = (function() {
  var this$1 = $m_s_util_hashing_MurmurHash3$();
  return this$1.aB(this.bT, this$1.ac);
});
$p.k = (function(that) {
  if ((that instanceof $c_scm_ArraySeq$ofDouble)) {
    var thatArray = that.bT;
    if ((this.bT === thatArray)) {
      return true;
    } else if ((this.bT.a.length === thatArray.a.length)) {
      var i = 0;
      while (((i < this.bT.a.length) && (this.bT.a[i] === thatArray.a[i]))) {
        i = ((1 + i) | 0);
      }
      return (i >= this.bT.a.length);
    } else {
      return false;
    }
  } else {
    return $c_scm_ArraySeq.prototype.k.call(this, that);
  }
});
$p.i = (function() {
  return new $c_sc_ArrayOps$ArrayIterator(this.bT);
});
$p.bY = (function() {
  return this.bT;
});
$p.a0 = (function() {
  return $m_s_reflect_ManifestFactory$DoubleManifest$();
});
$p.v = (function(i) {
  return this.fR(i);
});
$p.b = (function(v1) {
  return this.fR((v1 | 0));
});
function $isArrayOf_scm_ArraySeq$ofDouble(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.cf)));
}
var $d_scm_ArraySeq$ofDouble = new $TypeData().i($c_scm_ArraySeq$ofDouble, "scala.collection.mutable.ArraySeq$ofDouble", ({
  cf: 1,
  W: 1,
  L: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  J: 1,
  A: 1,
  H: 1,
  O: 1,
  N: 1,
  p: 1,
  o: 1,
  S: 1,
  R: 1,
  k: 1,
  q: 1,
  a: 1
}));
/** @constructor */
function $c_scm_ArraySeq$ofFloat(array) {
  this.bU = null;
  this.bU = array;
}
$p = $c_scm_ArraySeq$ofFloat.prototype = new $h_scm_ArraySeq();
$p.constructor = $c_scm_ArraySeq$ofFloat;
/** @constructor */
function $h_scm_ArraySeq$ofFloat() {
}
$h_scm_ArraySeq$ofFloat.prototype = $p;
$p.q = (function() {
  return this.bU.a.length;
});
$p.fS = (function(index) {
  return this.bU.a[index];
});
$p.r = (function() {
  var this$1 = $m_s_util_hashing_MurmurHash3$();
  return this$1.aB(this.bU, this$1.ac);
});
$p.k = (function(that) {
  if ((that instanceof $c_scm_ArraySeq$ofFloat)) {
    var thatArray = that.bU;
    if ((this.bU === thatArray)) {
      return true;
    } else if ((this.bU.a.length === thatArray.a.length)) {
      var i = 0;
      while (((i < this.bU.a.length) && (this.bU.a[i] === thatArray.a[i]))) {
        i = ((1 + i) | 0);
      }
      return (i >= this.bU.a.length);
    } else {
      return false;
    }
  } else {
    return $c_scm_ArraySeq.prototype.k.call(this, that);
  }
});
$p.i = (function() {
  return new $c_sc_ArrayOps$ArrayIterator(this.bU);
});
$p.bY = (function() {
  return this.bU;
});
$p.a0 = (function() {
  return $m_s_reflect_ManifestFactory$FloatManifest$();
});
$p.v = (function(i) {
  return this.fS(i);
});
$p.b = (function(v1) {
  return this.fS((v1 | 0));
});
function $isArrayOf_scm_ArraySeq$ofFloat(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.cg)));
}
var $d_scm_ArraySeq$ofFloat = new $TypeData().i($c_scm_ArraySeq$ofFloat, "scala.collection.mutable.ArraySeq$ofFloat", ({
  cg: 1,
  W: 1,
  L: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  J: 1,
  A: 1,
  H: 1,
  O: 1,
  N: 1,
  p: 1,
  o: 1,
  S: 1,
  R: 1,
  k: 1,
  q: 1,
  a: 1
}));
/** @constructor */
function $c_scm_ArraySeq$ofInt(array) {
  this.dp = null;
  this.dp = array;
}
$p = $c_scm_ArraySeq$ofInt.prototype = new $h_scm_ArraySeq();
$p.constructor = $c_scm_ArraySeq$ofInt;
/** @constructor */
function $h_scm_ArraySeq$ofInt() {
}
$h_scm_ArraySeq$ofInt.prototype = $p;
$p.q = (function() {
  return this.dp.a.length;
});
$p.fT = (function(index) {
  return this.dp.a[index];
});
$p.r = (function() {
  var this$1 = $m_s_util_hashing_MurmurHash3$();
  return this$1.aB(this.dp, this$1.ac);
});
$p.k = (function(that) {
  return ((that instanceof $c_scm_ArraySeq$ofInt) ? $m_ju_Arrays$().iU(this.dp, that.dp) : $c_scm_ArraySeq.prototype.k.call(this, that));
});
$p.i = (function() {
  return new $c_sc_ArrayOps$ArrayIterator(this.dp);
});
$p.bY = (function() {
  return this.dp;
});
$p.a0 = (function() {
  return $m_s_reflect_ManifestFactory$IntManifest$();
});
$p.v = (function(i) {
  return this.fT(i);
});
$p.b = (function(v1) {
  return this.fT((v1 | 0));
});
function $isArrayOf_scm_ArraySeq$ofInt(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.ch)));
}
var $d_scm_ArraySeq$ofInt = new $TypeData().i($c_scm_ArraySeq$ofInt, "scala.collection.mutable.ArraySeq$ofInt", ({
  ch: 1,
  W: 1,
  L: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  J: 1,
  A: 1,
  H: 1,
  O: 1,
  N: 1,
  p: 1,
  o: 1,
  S: 1,
  R: 1,
  k: 1,
  q: 1,
  a: 1
}));
/** @constructor */
function $c_scm_ArraySeq$ofLong(array) {
  this.dq = null;
  this.dq = array;
}
$p = $c_scm_ArraySeq$ofLong.prototype = new $h_scm_ArraySeq();
$p.constructor = $c_scm_ArraySeq$ofLong;
/** @constructor */
function $h_scm_ArraySeq$ofLong() {
}
$h_scm_ArraySeq$ofLong.prototype = $p;
$p.q = (function() {
  return ((this.dq.a.length >>> 1) | 0);
});
$p.fU = (function(index) {
  var $x_1 = this.dq.a;
  var $x_2 = (index << 1);
  return $bL($x_1[$x_2], $x_1[(($x_2 + 1) | 0)]);
});
$p.r = (function() {
  var this$1 = $m_s_util_hashing_MurmurHash3$();
  return this$1.aB(this.dq, this$1.ac);
});
$p.k = (function(that) {
  return ((that instanceof $c_scm_ArraySeq$ofLong) ? $m_ju_Arrays$().nq(this.dq, that.dq) : $c_scm_ArraySeq.prototype.k.call(this, that));
});
$p.i = (function() {
  return new $c_sc_ArrayOps$ArrayIterator(this.dq);
});
$p.bY = (function() {
  return this.dq;
});
$p.a0 = (function() {
  return $m_s_reflect_ManifestFactory$LongManifest$();
});
$p.v = (function(i) {
  return this.fU(i);
});
$p.b = (function(v1) {
  return this.fU((v1 | 0));
});
function $isArrayOf_scm_ArraySeq$ofLong(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.ci)));
}
var $d_scm_ArraySeq$ofLong = new $TypeData().i($c_scm_ArraySeq$ofLong, "scala.collection.mutable.ArraySeq$ofLong", ({
  ci: 1,
  W: 1,
  L: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  J: 1,
  A: 1,
  H: 1,
  O: 1,
  N: 1,
  p: 1,
  o: 1,
  S: 1,
  R: 1,
  k: 1,
  q: 1,
  a: 1
}));
/** @constructor */
function $c_scm_ArraySeq$ofRef(array) {
  this.cO = null;
  this.cO = array;
}
$p = $c_scm_ArraySeq$ofRef.prototype = new $h_scm_ArraySeq();
$p.constructor = $c_scm_ArraySeq$ofRef;
/** @constructor */
function $h_scm_ArraySeq$ofRef() {
}
$h_scm_ArraySeq$ofRef.prototype = $p;
$p.a0 = (function() {
  return $m_s_reflect_ClassTag$().n8($objectGetClass(this.cO).ah.Q());
});
$p.q = (function() {
  return this.cO.a.length;
});
$p.v = (function(index) {
  return this.cO.a[index];
});
$p.r = (function() {
  var this$1 = $m_s_util_hashing_MurmurHash3$();
  return this$1.aB(this.cO, this$1.ac);
});
$p.k = (function(that) {
  return ((that instanceof $c_scm_ArraySeq$ofRef) ? $m_s_Array$().nt(this.cO, that.cO) : $c_scm_ArraySeq.prototype.k.call(this, that));
});
$p.i = (function() {
  return new $c_sc_ArrayOps$ArrayIterator(this.cO);
});
$p.bY = (function() {
  return this.cO;
});
$p.b = (function(v1) {
  return this.v((v1 | 0));
});
function $isArrayOf_scm_ArraySeq$ofRef(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.cj)));
}
var $d_scm_ArraySeq$ofRef = new $TypeData().i($c_scm_ArraySeq$ofRef, "scala.collection.mutable.ArraySeq$ofRef", ({
  cj: 1,
  W: 1,
  L: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  J: 1,
  A: 1,
  H: 1,
  O: 1,
  N: 1,
  p: 1,
  o: 1,
  S: 1,
  R: 1,
  k: 1,
  q: 1,
  a: 1
}));
/** @constructor */
function $c_scm_ArraySeq$ofShort(array) {
  this.dr = null;
  this.dr = array;
}
$p = $c_scm_ArraySeq$ofShort.prototype = new $h_scm_ArraySeq();
$p.constructor = $c_scm_ArraySeq$ofShort;
/** @constructor */
function $h_scm_ArraySeq$ofShort() {
}
$h_scm_ArraySeq$ofShort.prototype = $p;
$p.q = (function() {
  return this.dr.a.length;
});
$p.fV = (function(index) {
  return this.dr.a[index];
});
$p.r = (function() {
  var this$1 = $m_s_util_hashing_MurmurHash3$();
  return this$1.aB(this.dr, this$1.ac);
});
$p.k = (function(that) {
  return ((that instanceof $c_scm_ArraySeq$ofShort) ? $m_ju_Arrays$().nr(this.dr, that.dr) : $c_scm_ArraySeq.prototype.k.call(this, that));
});
$p.i = (function() {
  return new $c_sc_ArrayOps$ArrayIterator(this.dr);
});
$p.bY = (function() {
  return this.dr;
});
$p.a0 = (function() {
  return $m_s_reflect_ManifestFactory$ShortManifest$();
});
$p.v = (function(i) {
  return this.fV(i);
});
$p.b = (function(v1) {
  return this.fV((v1 | 0));
});
function $isArrayOf_scm_ArraySeq$ofShort(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.ck)));
}
var $d_scm_ArraySeq$ofShort = new $TypeData().i($c_scm_ArraySeq$ofShort, "scala.collection.mutable.ArraySeq$ofShort", ({
  ck: 1,
  W: 1,
  L: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  J: 1,
  A: 1,
  H: 1,
  O: 1,
  N: 1,
  p: 1,
  o: 1,
  S: 1,
  R: 1,
  k: 1,
  q: 1,
  a: 1
}));
/** @constructor */
function $c_scm_ArraySeq$ofUnit(array) {
  this.dX = null;
  this.dX = array;
}
$p = $c_scm_ArraySeq$ofUnit.prototype = new $h_scm_ArraySeq();
$p.constructor = $c_scm_ArraySeq$ofUnit;
/** @constructor */
function $h_scm_ArraySeq$ofUnit() {
}
$h_scm_ArraySeq$ofUnit.prototype = $p;
$p.q = (function() {
  return this.dX.a.length;
});
$p.fW = (function(index) {
});
$p.r = (function() {
  var this$1 = $m_s_util_hashing_MurmurHash3$();
  return this$1.aB(this.dX, this$1.ac);
});
$p.k = (function(that) {
  return ((that instanceof $c_scm_ArraySeq$ofUnit) ? (this.dX.a.length === that.dX.a.length) : $c_scm_ArraySeq.prototype.k.call(this, that));
});
$p.i = (function() {
  return new $c_sc_ArrayOps$ArrayIterator(this.dX);
});
$p.bY = (function() {
  return this.dX;
});
$p.a0 = (function() {
  return $m_s_reflect_ManifestFactory$UnitManifest$();
});
$p.v = (function(i) {
  this.fW(i);
});
$p.b = (function(v1) {
  this.fW((v1 | 0));
});
function $isArrayOf_scm_ArraySeq$ofUnit(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.cl)));
}
var $d_scm_ArraySeq$ofUnit = new $TypeData().i($c_scm_ArraySeq$ofUnit, "scala.collection.mutable.ArraySeq$ofUnit", ({
  cl: 1,
  W: 1,
  L: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  J: 1,
  A: 1,
  H: 1,
  O: 1,
  N: 1,
  p: 1,
  o: 1,
  S: 1,
  R: 1,
  k: 1,
  q: 1,
  a: 1
}));
function $isArrayOf_scm_HashMap(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.gL)));
}
function $ct_sci_BigVector__AO__AO__I__($thiz, _prefix1, suffix1, length0) {
  $thiz.f = suffix1;
  $thiz.h = length0;
  $ct_sci_Vector__AO__($thiz, _prefix1);
  return $thiz;
}
/** @constructor */
function $c_sci_BigVector() {
  this.d = null;
  this.f = null;
  this.h = 0;
}
$p = $c_sci_BigVector.prototype = new $h_sci_VectorImpl();
$p.constructor = $c_sci_BigVector;
/** @constructor */
function $h_sci_BigVector() {
}
$h_sci_BigVector.prototype = $p;
function $isArrayOf_sci_BigVector(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.ae)));
}
/** @constructor */
function $c_sci_Vector1(_data1) {
  this.d = null;
  $ct_sci_Vector__AO__(this, _data1);
}
$p = $c_sci_Vector1.prototype = new $h_sci_VectorImpl();
$p.constructor = $c_sci_Vector1;
/** @constructor */
function $h_sci_Vector1() {
}
$h_sci_Vector1.prototype = $p;
$p.v = (function(index) {
  if (((index >= 0) && (index < this.d.a.length))) {
    return this.d.a[index];
  } else {
    throw this.aw(index);
  }
});
$p.dG = (function(index, elem) {
  if (((index >= 0) && (index < this.d.a.length))) {
    var a1 = this.d;
    var a1c = a1.e();
    a1c.a[index] = elem;
    return new $c_sci_Vector1(a1c);
  } else {
    throw this.aw(index);
  }
});
$p.dz = (function(elem) {
  if ((this.d.a.length < 32)) {
    return new $c_sci_Vector1($m_sci_VectorStatics$().eO(this.d, elem));
  } else {
    var $x_2 = this.d;
    var $x_1 = $m_sci_VectorStatics$().bk;
    var a = new $ac_O(1);
    a.a[0] = elem;
    return new $c_sci_Vector2($x_2, 32, $x_1, a, 33);
  }
});
$p.cx = (function() {
  return 1;
});
$p.cw = (function(idx) {
  return this.d;
});
$p.b = (function(v1) {
  var index = (v1 | 0);
  if (((index >= 0) && (index < this.d.a.length))) {
    return this.d.a[index];
  } else {
    throw this.aw(index);
  }
});
var $d_sci_Vector1 = new $TypeData().i($c_sci_Vector1, "scala.collection.immutable.Vector1", ({
  gq: 1,
  ag: 1,
  a6: 1,
  x: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  r: 1,
  w: 1,
  v: 1,
  p: 1,
  o: 1,
  C: 1,
  y: 1,
  k: 1,
  q: 1,
  z: 1,
  a: 1,
  U: 1
}));
/** @constructor */
function $c_sci_$colon$colon(head, next) {
  this.gI = null;
  this.J = null;
  this.gI = head;
  this.J = next;
}
$p = $c_sci_$colon$colon.prototype = new $h_sci_List();
$p.constructor = $c_sci_$colon$colon;
/** @constructor */
function $h_sci_$colon$colon() {
}
$h_sci_$colon$colon.prototype = $p;
$p.bx = (function() {
  return new $c_s_Product$$anon$1(this);
});
$p.aN = (function() {
  return 2;
});
$p.aP = (function() {
  return "::";
});
$p.aO = (function(n) {
  if ((n === 0)) {
    return this.gI;
  }
  if ((n === 1)) {
    return this.J;
  }
  throw $ct_jl_IndexOutOfBoundsException__I__(new $c_jl_IndexOutOfBoundsException(), n);
});
$p.n = (function() {
  return this.gI;
});
$p.nF = (function() {
  return new $c_s_Some(this.gI);
});
$p.l = (function() {
  return this.J;
});
var $d_sci_$colon$colon = new $TypeData().i($c_sci_$colon$colon, "scala.collection.immutable.$colon$colon", ({
  fK: 1,
  aQ: 1,
  x: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  r: 1,
  w: 1,
  v: 1,
  aK: 1,
  an: 1,
  aP: 1,
  aO: 1,
  k: 1,
  q: 1,
  bQ: 1,
  z: 1,
  a: 1,
  U: 1,
  E: 1
}));
/** @constructor */
function $c_sci_Nil$() {
  $n_sci_Nil$ = this;
  var _1 = $m_sci_Nil$();
  $m_sci_Nil$();
}
$p = $c_sci_Nil$.prototype = new $h_sci_List();
$p.constructor = $c_sci_Nil$;
/** @constructor */
function $h_sci_Nil$() {
}
$h_sci_Nil$.prototype = $p;
$p.bx = (function() {
  return new $c_s_Product$$anon$1(this);
});
$p.aN = (function() {
  return 0;
});
$p.aP = (function() {
  return "Nil";
});
$p.aO = (function(n) {
  throw $ct_jl_IndexOutOfBoundsException__I__(new $c_jl_IndexOutOfBoundsException(), n);
});
$p.qh = (function() {
  throw $ct_ju_NoSuchElementException__T__(new $c_ju_NoSuchElementException(), "head of empty list");
});
$p.rs = (function() {
  throw new $c_jl_UnsupportedOperationException("tail of empty list");
});
$p.x = (function() {
  return 0;
});
$p.i = (function() {
  return $m_sc_Iterator$().O;
});
$p.n = (function() {
  this.qh();
});
$p.nF = (function() {
  return $m_s_None$();
});
$p.l = (function() {
  this.rs();
});
var $d_sci_Nil$ = new $TypeData().i($c_sci_Nil$, "scala.collection.immutable.Nil$", ({
  gg: 1,
  aQ: 1,
  x: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  r: 1,
  w: 1,
  v: 1,
  aK: 1,
  an: 1,
  aP: 1,
  aO: 1,
  k: 1,
  q: 1,
  bQ: 1,
  z: 1,
  a: 1,
  U: 1,
  E: 1
}));
var $n_sci_Nil$;
function $m_sci_Nil$() {
  if ((!$n_sci_Nil$)) {
    $n_sci_Nil$ = new $c_sci_Nil$();
  }
  return $n_sci_Nil$;
}
/** @constructor */
function $c_sci_Vector0$() {
  this.d = null;
  this.f = null;
  this.h = 0;
  $ct_sci_BigVector__AO__AO__I__(this, $m_sci_VectorStatics$().ip, $m_sci_VectorStatics$().ip, 0);
}
$p = $c_sci_Vector0$.prototype = new $h_sci_BigVector();
$p.constructor = $c_sci_Vector0$;
/** @constructor */
function $h_sci_Vector0$() {
}
$h_sci_Vector0$.prototype = $p;
$p.n7 = (function(index) {
  throw this.aw(index);
});
$p.dG = (function(index, elem) {
  throw this.aw(index);
});
$p.dz = (function(elem) {
  var a = new $ac_O(1);
  a.a[0] = elem;
  return new $c_sci_Vector1(a);
});
$p.cx = (function() {
  return 0;
});
$p.cw = (function(idx) {
  return null;
});
$p.k = (function(o) {
  return ((this === o) || ((o instanceof $c_sci_Vector) ? false : $f_sc_Seq__equals__O__Z(this, o)));
});
$p.aw = (function(index) {
  return $ct_jl_IndexOutOfBoundsException__T__(new $c_jl_IndexOutOfBoundsException(), (index + " is out of bounds (empty vector)"));
});
$p.v = (function(i) {
  this.n7(i);
});
$p.b = (function(v1) {
  this.n7((v1 | 0));
});
var $d_sci_Vector0$ = new $TypeData().i($c_sci_Vector0$, "scala.collection.immutable.Vector0$", ({
  gp: 1,
  ae: 1,
  ag: 1,
  a6: 1,
  x: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  r: 1,
  w: 1,
  v: 1,
  p: 1,
  o: 1,
  C: 1,
  y: 1,
  k: 1,
  q: 1,
  z: 1,
  a: 1,
  U: 1
}));
var $n_sci_Vector0$;
function $m_sci_Vector0$() {
  if ((!$n_sci_Vector0$)) {
    $n_sci_Vector0$ = new $c_sci_Vector0$();
  }
  return $n_sci_Vector0$;
}
/** @constructor */
function $c_sci_Vector2(_prefix1, len1, data2, _suffix1, _length0) {
  this.d = null;
  this.f = null;
  this.h = 0;
  this.bG = 0;
  this.bj = null;
  this.bG = len1;
  this.bj = data2;
  $ct_sci_BigVector__AO__AO__I__(this, _prefix1, _suffix1, _length0);
}
$p = $c_sci_Vector2.prototype = new $h_sci_BigVector();
$p.constructor = $c_sci_Vector2;
/** @constructor */
function $h_sci_Vector2() {
}
$h_sci_Vector2.prototype = $p;
$p.v = (function(index) {
  if (((index >= 0) && (index < this.h))) {
    var io = ((index - this.bG) | 0);
    if ((io >= 0)) {
      var i2 = ((io >>> 5) | 0);
      var i1 = (31 & io);
      return ((i2 < this.bj.a.length) ? this.bj.a[i2].a[i1] : this.f.a[(31 & io)]);
    } else {
      return this.d.a[index];
    }
  } else {
    throw this.aw(index);
  }
});
$p.dG = (function(index, elem) {
  if (((index >= 0) && (index < this.h))) {
    if ((index >= this.bG)) {
      var io = ((index - this.bG) | 0);
      var i2 = ((io >>> 5) | 0);
      var i1 = (31 & io);
      if ((i2 < this.bj.a.length)) {
        var a2 = this.bj;
        var a2c = a2.e();
        var a1 = a2c.a[i2];
        var a1c = a1.e();
        a1c.a[i1] = elem;
        a2c.a[i2] = a1c;
        return new $c_sci_Vector2(this.d, this.bG, a2c, this.f, this.h);
      } else {
        var a1$1 = this.f;
        var a1c$1 = a1$1.e();
        a1c$1.a[i1] = elem;
        return new $c_sci_Vector2(this.d, this.bG, this.bj, a1c$1, this.h);
      }
    } else {
      var a1$2 = this.d;
      var a1c$2 = a1$2.e();
      a1c$2.a[index] = elem;
      return new $c_sci_Vector2(a1c$2, this.bG, this.bj, this.f, this.h);
    }
  } else {
    throw this.aw(index);
  }
});
$p.dz = (function(elem) {
  if ((this.f.a.length < 32)) {
    var suffix1$3 = $m_sci_VectorStatics$().eO(this.f, elem);
    var length0$3 = ((1 + this.h) | 0);
    return new $c_sci_Vector2(this.d, this.bG, this.bj, suffix1$3, length0$3);
  } else if ((this.bj.a.length < 30)) {
    var data2$4 = $m_sci_VectorStatics$().z(this.bj, this.f);
    var a = new $ac_O(1);
    a.a[0] = elem;
    var length0$4 = ((1 + this.h) | 0);
    return new $c_sci_Vector2(this.d, this.bG, data2$4, a, length0$4);
  } else {
    var $x_5 = this.d;
    var $x_4 = this.bG;
    var $x_3 = this.bj;
    var $x_2 = this.bG;
    var $x_1 = $m_sci_VectorStatics$().cm;
    var x = this.f;
    var a$1 = new ($d_O.r().r().C)(1);
    a$1.a[0] = x;
    var a$2 = new $ac_O(1);
    a$2.a[0] = elem;
    return new $c_sci_Vector3($x_5, $x_4, $x_3, ((960 + $x_2) | 0), $x_1, a$1, a$2, ((1 + this.h) | 0));
  }
});
$p.cx = (function() {
  return 3;
});
$p.cw = (function(idx) {
  switch (idx) {
    case 0: {
      return this.d;
      break;
    }
    case 1: {
      return this.bj;
      break;
    }
    case 2: {
      return this.f;
      break;
    }
    default: {
      throw new $c_s_MatchError(idx);
    }
  }
});
$p.b = (function(v1) {
  var index = (v1 | 0);
  if (((index >= 0) && (index < this.h))) {
    var io = ((index - this.bG) | 0);
    if ((io >= 0)) {
      var i2 = ((io >>> 5) | 0);
      var i1 = (31 & io);
      return ((i2 < this.bj.a.length) ? this.bj.a[i2].a[i1] : this.f.a[(31 & io)]);
    } else {
      return this.d.a[index];
    }
  } else {
    throw this.aw(index);
  }
});
var $d_sci_Vector2 = new $TypeData().i($c_sci_Vector2, "scala.collection.immutable.Vector2", ({
  gr: 1,
  ae: 1,
  ag: 1,
  a6: 1,
  x: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  r: 1,
  w: 1,
  v: 1,
  p: 1,
  o: 1,
  C: 1,
  y: 1,
  k: 1,
  q: 1,
  z: 1,
  a: 1,
  U: 1
}));
/** @constructor */
function $c_sci_Vector3(_prefix1, len1, prefix2, len12, data3, suffix2, _suffix1, _length0) {
  this.d = null;
  this.f = null;
  this.h = 0;
  this.b9 = 0;
  this.bw = null;
  this.ba = 0;
  this.aR = null;
  this.aS = null;
  this.b9 = len1;
  this.bw = prefix2;
  this.ba = len12;
  this.aR = data3;
  this.aS = suffix2;
  $ct_sci_BigVector__AO__AO__I__(this, _prefix1, _suffix1, _length0);
}
$p = $c_sci_Vector3.prototype = new $h_sci_BigVector();
$p.constructor = $c_sci_Vector3;
/** @constructor */
function $h_sci_Vector3() {
}
$h_sci_Vector3.prototype = $p;
$p.v = (function(index) {
  if (((index >= 0) && (index < this.h))) {
    var io = ((index - this.ba) | 0);
    if ((io >= 0)) {
      var i3 = ((io >>> 10) | 0);
      var i2 = (31 & ((io >>> 5) | 0));
      var i1 = (31 & io);
      return ((i3 < this.aR.a.length) ? this.aR.a[i3].a[i2].a[i1] : ((i2 < this.aS.a.length) ? this.aS.a[i2].a[i1] : this.f.a[i1]));
    } else if ((index >= this.b9)) {
      var io$2 = ((index - this.b9) | 0);
      return this.bw.a[((io$2 >>> 5) | 0)].a[(31 & io$2)];
    } else {
      return this.d.a[index];
    }
  } else {
    throw this.aw(index);
  }
});
$p.dG = (function(index, elem) {
  if (((index >= 0) && (index < this.h))) {
    if ((index >= this.ba)) {
      var io = ((index - this.ba) | 0);
      var i3 = ((io >>> 10) | 0);
      var i2 = (31 & ((io >>> 5) | 0));
      var i1 = (31 & io);
      if ((i3 < this.aR.a.length)) {
        var a3 = this.aR;
        var a3c = a3.e();
        var a2 = a3c.a[i3];
        var a2c = a2.e();
        var a1 = a2c.a[i2];
        var a1c = a1.e();
        a1c.a[i1] = elem;
        a2c.a[i2] = a1c;
        a3c.a[i3] = a2c;
        return new $c_sci_Vector3(this.d, this.b9, this.bw, this.ba, a3c, this.aS, this.f, this.h);
      } else if ((i2 < this.aS.a.length)) {
        var a2$1 = this.aS;
        var a2c$1 = a2$1.e();
        var a1$1 = a2c$1.a[i2];
        var a1c$1 = a1$1.e();
        a1c$1.a[i1] = elem;
        a2c$1.a[i2] = a1c$1;
        return new $c_sci_Vector3(this.d, this.b9, this.bw, this.ba, this.aR, a2c$1, this.f, this.h);
      } else {
        var a1$2 = this.f;
        var a1c$2 = a1$2.e();
        a1c$2.a[i1] = elem;
        return new $c_sci_Vector3(this.d, this.b9, this.bw, this.ba, this.aR, this.aS, a1c$2, this.h);
      }
    } else if ((index >= this.b9)) {
      var io$2 = ((index - this.b9) | 0);
      var a2$2 = this.bw;
      var idx2 = ((io$2 >>> 5) | 0);
      var idx1 = (31 & io$2);
      var a2c$2 = a2$2.e();
      var a1$3 = a2c$2.a[idx2];
      var a1c$3 = a1$3.e();
      a1c$3.a[idx1] = elem;
      a2c$2.a[idx2] = a1c$3;
      return new $c_sci_Vector3(this.d, this.b9, a2c$2, this.ba, this.aR, this.aS, this.f, this.h);
    } else {
      var a1$4 = this.d;
      var a1c$4 = a1$4.e();
      a1c$4.a[index] = elem;
      return new $c_sci_Vector3(a1c$4, this.b9, this.bw, this.ba, this.aR, this.aS, this.f, this.h);
    }
  } else {
    throw this.aw(index);
  }
});
$p.dz = (function(elem) {
  if ((this.f.a.length < 32)) {
    var suffix1$16 = $m_sci_VectorStatics$().eO(this.f, elem);
    var length0$16 = ((1 + this.h) | 0);
    return new $c_sci_Vector3(this.d, this.b9, this.bw, this.ba, this.aR, this.aS, suffix1$16, length0$16);
  } else if ((this.aS.a.length < 31)) {
    var suffix2$6 = $m_sci_VectorStatics$().z(this.aS, this.f);
    var a = new $ac_O(1);
    a.a[0] = elem;
    var length0$17 = ((1 + this.h) | 0);
    return new $c_sci_Vector3(this.d, this.b9, this.bw, this.ba, this.aR, suffix2$6, a, length0$17);
  } else if ((this.aR.a.length < 30)) {
    var data3$7 = $m_sci_VectorStatics$().z(this.aR, $m_sci_VectorStatics$().z(this.aS, this.f));
    var a$1 = new $ac_O(1);
    a$1.a[0] = elem;
    var length0$18 = ((1 + this.h) | 0);
    return new $c_sci_Vector3(this.d, this.b9, this.bw, this.ba, data3$7, $m_sci_VectorStatics$().bk, a$1, length0$18);
  } else {
    var $x_8 = this.d;
    var $x_7 = this.b9;
    var $x_6 = this.bw;
    var $x_5 = this.ba;
    var $x_4 = this.aR;
    var $x_3 = this.ba;
    var $x_2 = $m_sci_VectorStatics$().eC;
    var x = $m_sci_VectorStatics$().z(this.aS, this.f);
    var a$2 = new ($d_O.r().r().r().C)(1);
    a$2.a[0] = x;
    var $x_1 = $m_sci_VectorStatics$().bk;
    var a$3 = new $ac_O(1);
    a$3.a[0] = elem;
    return new $c_sci_Vector4($x_8, $x_7, $x_6, $x_5, $x_4, ((30720 + $x_3) | 0), $x_2, a$2, $x_1, a$3, ((1 + this.h) | 0));
  }
});
$p.cx = (function() {
  return 5;
});
$p.cw = (function(idx) {
  switch (idx) {
    case 0: {
      return this.d;
      break;
    }
    case 1: {
      return this.bw;
      break;
    }
    case 2: {
      return this.aR;
      break;
    }
    case 3: {
      return this.aS;
      break;
    }
    case 4: {
      return this.f;
      break;
    }
    default: {
      throw new $c_s_MatchError(idx);
    }
  }
});
$p.b = (function(v1) {
  var index = (v1 | 0);
  if (((index >= 0) && (index < this.h))) {
    var io = ((index - this.ba) | 0);
    if ((io >= 0)) {
      var i3 = ((io >>> 10) | 0);
      var i2 = (31 & ((io >>> 5) | 0));
      var i1 = (31 & io);
      return ((i3 < this.aR.a.length) ? this.aR.a[i3].a[i2].a[i1] : ((i2 < this.aS.a.length) ? this.aS.a[i2].a[i1] : this.f.a[i1]));
    } else if ((index >= this.b9)) {
      var io$2 = ((index - this.b9) | 0);
      return this.bw.a[((io$2 >>> 5) | 0)].a[(31 & io$2)];
    } else {
      return this.d.a[index];
    }
  } else {
    throw this.aw(index);
  }
});
var $d_sci_Vector3 = new $TypeData().i($c_sci_Vector3, "scala.collection.immutable.Vector3", ({
  gs: 1,
  ae: 1,
  ag: 1,
  a6: 1,
  x: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  r: 1,
  w: 1,
  v: 1,
  p: 1,
  o: 1,
  C: 1,
  y: 1,
  k: 1,
  q: 1,
  z: 1,
  a: 1,
  U: 1
}));
/** @constructor */
function $c_sci_Vector4(_prefix1, len1, prefix2, len12, prefix3, len123, data4, suffix3, suffix2, _suffix1, _length0) {
  this.d = null;
  this.f = null;
  this.h = 0;
  this.aH = 0;
  this.b0 = null;
  this.aI = 0;
  this.b1 = null;
  this.aJ = 0;
  this.as = null;
  this.au = null;
  this.at = null;
  this.aH = len1;
  this.b0 = prefix2;
  this.aI = len12;
  this.b1 = prefix3;
  this.aJ = len123;
  this.as = data4;
  this.au = suffix3;
  this.at = suffix2;
  $ct_sci_BigVector__AO__AO__I__(this, _prefix1, _suffix1, _length0);
}
$p = $c_sci_Vector4.prototype = new $h_sci_BigVector();
$p.constructor = $c_sci_Vector4;
/** @constructor */
function $h_sci_Vector4() {
}
$h_sci_Vector4.prototype = $p;
$p.v = (function(index) {
  if (((index >= 0) && (index < this.h))) {
    var io = ((index - this.aJ) | 0);
    if ((io >= 0)) {
      var i4 = ((io >>> 15) | 0);
      var i3 = (31 & ((io >>> 10) | 0));
      var i2 = (31 & ((io >>> 5) | 0));
      var i1 = (31 & io);
      return ((i4 < this.as.a.length) ? this.as.a[i4].a[i3].a[i2].a[i1] : ((i3 < this.au.a.length) ? this.au.a[i3].a[i2].a[i1] : ((i2 < this.at.a.length) ? this.at.a[i2].a[i1] : this.f.a[i1])));
    } else if ((index >= this.aI)) {
      var io$2 = ((index - this.aI) | 0);
      return this.b1.a[((io$2 >>> 10) | 0)].a[(31 & ((io$2 >>> 5) | 0))].a[(31 & io$2)];
    } else if ((index >= this.aH)) {
      var io$3 = ((index - this.aH) | 0);
      return this.b0.a[((io$3 >>> 5) | 0)].a[(31 & io$3)];
    } else {
      return this.d.a[index];
    }
  } else {
    throw this.aw(index);
  }
});
$p.dG = (function(index, elem) {
  if (((index >= 0) && (index < this.h))) {
    if ((index >= this.aJ)) {
      var io = ((index - this.aJ) | 0);
      var i4 = ((io >>> 15) | 0);
      var i3 = (31 & ((io >>> 10) | 0));
      var i2 = (31 & ((io >>> 5) | 0));
      var i1 = (31 & io);
      if ((i4 < this.as.a.length)) {
        var a4 = this.as;
        var a4c = a4.e();
        var a3 = a4c.a[i4];
        var a3c = a3.e();
        var a2 = a3c.a[i3];
        var a2c = a2.e();
        var a1 = a2c.a[i2];
        var a1c = a1.e();
        a1c.a[i1] = elem;
        a2c.a[i2] = a1c;
        a3c.a[i3] = a2c;
        a4c.a[i4] = a3c;
        return new $c_sci_Vector4(this.d, this.aH, this.b0, this.aI, this.b1, this.aJ, a4c, this.au, this.at, this.f, this.h);
      } else if ((i3 < this.au.a.length)) {
        var a3$1 = this.au;
        var a3c$1 = a3$1.e();
        var a2$1 = a3c$1.a[i3];
        var a2c$1 = a2$1.e();
        var a1$1 = a2c$1.a[i2];
        var a1c$1 = a1$1.e();
        a1c$1.a[i1] = elem;
        a2c$1.a[i2] = a1c$1;
        a3c$1.a[i3] = a2c$1;
        return new $c_sci_Vector4(this.d, this.aH, this.b0, this.aI, this.b1, this.aJ, this.as, a3c$1, this.at, this.f, this.h);
      } else if ((i2 < this.at.a.length)) {
        var a2$2 = this.at;
        var a2c$2 = a2$2.e();
        var a1$2 = a2c$2.a[i2];
        var a1c$2 = a1$2.e();
        a1c$2.a[i1] = elem;
        a2c$2.a[i2] = a1c$2;
        return new $c_sci_Vector4(this.d, this.aH, this.b0, this.aI, this.b1, this.aJ, this.as, this.au, a2c$2, this.f, this.h);
      } else {
        var a1$3 = this.f;
        var a1c$3 = a1$3.e();
        a1c$3.a[i1] = elem;
        return new $c_sci_Vector4(this.d, this.aH, this.b0, this.aI, this.b1, this.aJ, this.as, this.au, this.at, a1c$3, this.h);
      }
    } else if ((index >= this.aI)) {
      var io$2 = ((index - this.aI) | 0);
      var a3$2 = this.b1;
      var idx3 = ((io$2 >>> 10) | 0);
      var idx2 = (31 & ((io$2 >>> 5) | 0));
      var idx1 = (31 & io$2);
      var a3c$2 = a3$2.e();
      var a2$3 = a3c$2.a[idx3];
      var a2c$3 = a2$3.e();
      var a1$4 = a2c$3.a[idx2];
      var a1c$4 = a1$4.e();
      a1c$4.a[idx1] = elem;
      a2c$3.a[idx2] = a1c$4;
      a3c$2.a[idx3] = a2c$3;
      return new $c_sci_Vector4(this.d, this.aH, this.b0, this.aI, a3c$2, this.aJ, this.as, this.au, this.at, this.f, this.h);
    } else if ((index >= this.aH)) {
      var io$3 = ((index - this.aH) | 0);
      var a2$4 = this.b0;
      var idx2$1 = ((io$3 >>> 5) | 0);
      var idx1$1 = (31 & io$3);
      var a2c$4 = a2$4.e();
      var a1$5 = a2c$4.a[idx2$1];
      var a1c$5 = a1$5.e();
      a1c$5.a[idx1$1] = elem;
      a2c$4.a[idx2$1] = a1c$5;
      return new $c_sci_Vector4(this.d, this.aH, a2c$4, this.aI, this.b1, this.aJ, this.as, this.au, this.at, this.f, this.h);
    } else {
      var a1$6 = this.d;
      var a1c$6 = a1$6.e();
      a1c$6.a[index] = elem;
      return new $c_sci_Vector4(a1c$6, this.aH, this.b0, this.aI, this.b1, this.aJ, this.as, this.au, this.at, this.f, this.h);
    }
  } else {
    throw this.aw(index);
  }
});
$p.dz = (function(elem) {
  if ((this.f.a.length < 32)) {
    var suffix1$33 = $m_sci_VectorStatics$().eO(this.f, elem);
    var length0$33 = ((1 + this.h) | 0);
    return new $c_sci_Vector4(this.d, this.aH, this.b0, this.aI, this.b1, this.aJ, this.as, this.au, this.at, suffix1$33, length0$33);
  } else if ((this.at.a.length < 31)) {
    var suffix2$22 = $m_sci_VectorStatics$().z(this.at, this.f);
    var a = new $ac_O(1);
    a.a[0] = elem;
    var length0$34 = ((1 + this.h) | 0);
    return new $c_sci_Vector4(this.d, this.aH, this.b0, this.aI, this.b1, this.aJ, this.as, this.au, suffix2$22, a, length0$34);
  } else if ((this.au.a.length < 31)) {
    var suffix3$9 = $m_sci_VectorStatics$().z(this.au, $m_sci_VectorStatics$().z(this.at, this.f));
    var a$1 = new $ac_O(1);
    a$1.a[0] = elem;
    var length0$35 = ((1 + this.h) | 0);
    return new $c_sci_Vector4(this.d, this.aH, this.b0, this.aI, this.b1, this.aJ, this.as, suffix3$9, $m_sci_VectorStatics$().bk, a$1, length0$35);
  } else if ((this.as.a.length < 30)) {
    var data4$10 = $m_sci_VectorStatics$().z(this.as, $m_sci_VectorStatics$().z(this.au, $m_sci_VectorStatics$().z(this.at, this.f)));
    var a$2 = new $ac_O(1);
    a$2.a[0] = elem;
    var length0$36 = ((1 + this.h) | 0);
    return new $c_sci_Vector4(this.d, this.aH, this.b0, this.aI, this.b1, this.aJ, data4$10, $m_sci_VectorStatics$().cm, $m_sci_VectorStatics$().bk, a$2, length0$36);
  } else {
    var $x_11 = this.d;
    var $x_10 = this.aH;
    var $x_9 = this.b0;
    var $x_8 = this.aI;
    var $x_7 = this.b1;
    var $x_6 = this.aJ;
    var $x_5 = this.as;
    var $x_4 = this.aJ;
    var $x_3 = $m_sci_VectorStatics$().iq;
    var x = $m_sci_VectorStatics$().z(this.au, $m_sci_VectorStatics$().z(this.at, this.f));
    var a$3 = new ($d_O.r().r().r().r().C)(1);
    a$3.a[0] = x;
    var $x_2 = $m_sci_VectorStatics$().cm;
    var $x_1 = $m_sci_VectorStatics$().bk;
    var a$4 = new $ac_O(1);
    a$4.a[0] = elem;
    return new $c_sci_Vector5($x_11, $x_10, $x_9, $x_8, $x_7, $x_6, $x_5, ((983040 + $x_4) | 0), $x_3, a$3, $x_2, $x_1, a$4, ((1 + this.h) | 0));
  }
});
$p.cx = (function() {
  return 7;
});
$p.cw = (function(idx) {
  switch (idx) {
    case 0: {
      return this.d;
      break;
    }
    case 1: {
      return this.b0;
      break;
    }
    case 2: {
      return this.b1;
      break;
    }
    case 3: {
      return this.as;
      break;
    }
    case 4: {
      return this.au;
      break;
    }
    case 5: {
      return this.at;
      break;
    }
    case 6: {
      return this.f;
      break;
    }
    default: {
      throw new $c_s_MatchError(idx);
    }
  }
});
$p.b = (function(v1) {
  var index = (v1 | 0);
  if (((index >= 0) && (index < this.h))) {
    var io = ((index - this.aJ) | 0);
    if ((io >= 0)) {
      var i4 = ((io >>> 15) | 0);
      var i3 = (31 & ((io >>> 10) | 0));
      var i2 = (31 & ((io >>> 5) | 0));
      var i1 = (31 & io);
      return ((i4 < this.as.a.length) ? this.as.a[i4].a[i3].a[i2].a[i1] : ((i3 < this.au.a.length) ? this.au.a[i3].a[i2].a[i1] : ((i2 < this.at.a.length) ? this.at.a[i2].a[i1] : this.f.a[i1])));
    } else if ((index >= this.aI)) {
      var io$2 = ((index - this.aI) | 0);
      return this.b1.a[((io$2 >>> 10) | 0)].a[(31 & ((io$2 >>> 5) | 0))].a[(31 & io$2)];
    } else if ((index >= this.aH)) {
      var io$3 = ((index - this.aH) | 0);
      return this.b0.a[((io$3 >>> 5) | 0)].a[(31 & io$3)];
    } else {
      return this.d.a[index];
    }
  } else {
    throw this.aw(index);
  }
});
var $d_sci_Vector4 = new $TypeData().i($c_sci_Vector4, "scala.collection.immutable.Vector4", ({
  gt: 1,
  ae: 1,
  ag: 1,
  a6: 1,
  x: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  r: 1,
  w: 1,
  v: 1,
  p: 1,
  o: 1,
  C: 1,
  y: 1,
  k: 1,
  q: 1,
  z: 1,
  a: 1,
  U: 1
}));
/** @constructor */
function $c_sci_Vector5(_prefix1, len1, prefix2, len12, prefix3, len123, prefix4, len1234, data5, suffix4, suffix3, suffix2, _suffix1, _length0) {
  this.d = null;
  this.f = null;
  this.h = 0;
  this.aj = 0;
  this.ay = null;
  this.ak = 0;
  this.az = null;
  this.al = 0;
  this.aA = null;
  this.am = 0;
  this.a3 = null;
  this.a6 = null;
  this.a5 = null;
  this.a4 = null;
  this.aj = len1;
  this.ay = prefix2;
  this.ak = len12;
  this.az = prefix3;
  this.al = len123;
  this.aA = prefix4;
  this.am = len1234;
  this.a3 = data5;
  this.a6 = suffix4;
  this.a5 = suffix3;
  this.a4 = suffix2;
  $ct_sci_BigVector__AO__AO__I__(this, _prefix1, _suffix1, _length0);
}
$p = $c_sci_Vector5.prototype = new $h_sci_BigVector();
$p.constructor = $c_sci_Vector5;
/** @constructor */
function $h_sci_Vector5() {
}
$h_sci_Vector5.prototype = $p;
$p.v = (function(index) {
  if (((index >= 0) && (index < this.h))) {
    var io = ((index - this.am) | 0);
    if ((io >= 0)) {
      var i5 = ((io >>> 20) | 0);
      var i4 = (31 & ((io >>> 15) | 0));
      var i3 = (31 & ((io >>> 10) | 0));
      var i2 = (31 & ((io >>> 5) | 0));
      var i1 = (31 & io);
      return ((i5 < this.a3.a.length) ? this.a3.a[i5].a[i4].a[i3].a[i2].a[i1] : ((i4 < this.a6.a.length) ? this.a6.a[i4].a[i3].a[i2].a[i1] : ((i3 < this.a5.a.length) ? this.a5.a[i3].a[i2].a[i1] : ((i2 < this.a4.a.length) ? this.a4.a[i2].a[i1] : this.f.a[i1]))));
    } else if ((index >= this.al)) {
      var io$2 = ((index - this.al) | 0);
      return this.aA.a[((io$2 >>> 15) | 0)].a[(31 & ((io$2 >>> 10) | 0))].a[(31 & ((io$2 >>> 5) | 0))].a[(31 & io$2)];
    } else if ((index >= this.ak)) {
      var io$3 = ((index - this.ak) | 0);
      return this.az.a[((io$3 >>> 10) | 0)].a[(31 & ((io$3 >>> 5) | 0))].a[(31 & io$3)];
    } else if ((index >= this.aj)) {
      var io$4 = ((index - this.aj) | 0);
      return this.ay.a[((io$4 >>> 5) | 0)].a[(31 & io$4)];
    } else {
      return this.d.a[index];
    }
  } else {
    throw this.aw(index);
  }
});
$p.dG = (function(index, elem) {
  if (((index >= 0) && (index < this.h))) {
    if ((index >= this.am)) {
      var io = ((index - this.am) | 0);
      var i5 = ((io >>> 20) | 0);
      var i4 = (31 & ((io >>> 15) | 0));
      var i3 = (31 & ((io >>> 10) | 0));
      var i2 = (31 & ((io >>> 5) | 0));
      var i1 = (31 & io);
      if ((i5 < this.a3.a.length)) {
        var a5 = this.a3;
        var a5c = a5.e();
        var a4 = a5c.a[i5];
        var a4c = a4.e();
        var a3 = a4c.a[i4];
        var a3c = a3.e();
        var a2 = a3c.a[i3];
        var a2c = a2.e();
        var a1 = a2c.a[i2];
        var a1c = a1.e();
        a1c.a[i1] = elem;
        a2c.a[i2] = a1c;
        a3c.a[i3] = a2c;
        a4c.a[i4] = a3c;
        a5c.a[i5] = a4c;
        return new $c_sci_Vector5(this.d, this.aj, this.ay, this.ak, this.az, this.al, this.aA, this.am, a5c, this.a6, this.a5, this.a4, this.f, this.h);
      } else if ((i4 < this.a6.a.length)) {
        var a4$1 = this.a6;
        var a4c$1 = a4$1.e();
        var a3$1 = a4c$1.a[i4];
        var a3c$1 = a3$1.e();
        var a2$1 = a3c$1.a[i3];
        var a2c$1 = a2$1.e();
        var a1$1 = a2c$1.a[i2];
        var a1c$1 = a1$1.e();
        a1c$1.a[i1] = elem;
        a2c$1.a[i2] = a1c$1;
        a3c$1.a[i3] = a2c$1;
        a4c$1.a[i4] = a3c$1;
        return new $c_sci_Vector5(this.d, this.aj, this.ay, this.ak, this.az, this.al, this.aA, this.am, this.a3, a4c$1, this.a5, this.a4, this.f, this.h);
      } else if ((i3 < this.a5.a.length)) {
        var a3$2 = this.a5;
        var a3c$2 = a3$2.e();
        var a2$2 = a3c$2.a[i3];
        var a2c$2 = a2$2.e();
        var a1$2 = a2c$2.a[i2];
        var a1c$2 = a1$2.e();
        a1c$2.a[i1] = elem;
        a2c$2.a[i2] = a1c$2;
        a3c$2.a[i3] = a2c$2;
        return new $c_sci_Vector5(this.d, this.aj, this.ay, this.ak, this.az, this.al, this.aA, this.am, this.a3, this.a6, a3c$2, this.a4, this.f, this.h);
      } else if ((i2 < this.a4.a.length)) {
        var a2$3 = this.a4;
        var a2c$3 = a2$3.e();
        var a1$3 = a2c$3.a[i2];
        var a1c$3 = a1$3.e();
        a1c$3.a[i1] = elem;
        a2c$3.a[i2] = a1c$3;
        return new $c_sci_Vector5(this.d, this.aj, this.ay, this.ak, this.az, this.al, this.aA, this.am, this.a3, this.a6, this.a5, a2c$3, this.f, this.h);
      } else {
        var a1$4 = this.f;
        var a1c$4 = a1$4.e();
        a1c$4.a[i1] = elem;
        return new $c_sci_Vector5(this.d, this.aj, this.ay, this.ak, this.az, this.al, this.aA, this.am, this.a3, this.a6, this.a5, this.a4, a1c$4, this.h);
      }
    } else if ((index >= this.al)) {
      var io$2 = ((index - this.al) | 0);
      var a4$2 = this.aA;
      var idx4 = ((io$2 >>> 15) | 0);
      var idx3 = (31 & ((io$2 >>> 10) | 0));
      var idx2 = (31 & ((io$2 >>> 5) | 0));
      var idx1 = (31 & io$2);
      var a4c$2 = a4$2.e();
      var a3$3 = a4c$2.a[idx4];
      var a3c$3 = a3$3.e();
      var a2$4 = a3c$3.a[idx3];
      var a2c$4 = a2$4.e();
      var a1$5 = a2c$4.a[idx2];
      var a1c$5 = a1$5.e();
      a1c$5.a[idx1] = elem;
      a2c$4.a[idx2] = a1c$5;
      a3c$3.a[idx3] = a2c$4;
      a4c$2.a[idx4] = a3c$3;
      return new $c_sci_Vector5(this.d, this.aj, this.ay, this.ak, this.az, this.al, a4c$2, this.am, this.a3, this.a6, this.a5, this.a4, this.f, this.h);
    } else if ((index >= this.ak)) {
      var io$3 = ((index - this.ak) | 0);
      var a3$4 = this.az;
      var idx3$1 = ((io$3 >>> 10) | 0);
      var idx2$1 = (31 & ((io$3 >>> 5) | 0));
      var idx1$1 = (31 & io$3);
      var a3c$4 = a3$4.e();
      var a2$5 = a3c$4.a[idx3$1];
      var a2c$5 = a2$5.e();
      var a1$6 = a2c$5.a[idx2$1];
      var a1c$6 = a1$6.e();
      a1c$6.a[idx1$1] = elem;
      a2c$5.a[idx2$1] = a1c$6;
      a3c$4.a[idx3$1] = a2c$5;
      return new $c_sci_Vector5(this.d, this.aj, this.ay, this.ak, a3c$4, this.al, this.aA, this.am, this.a3, this.a6, this.a5, this.a4, this.f, this.h);
    } else if ((index >= this.aj)) {
      var io$4 = ((index - this.aj) | 0);
      var a2$6 = this.ay;
      var idx2$2 = ((io$4 >>> 5) | 0);
      var idx1$2 = (31 & io$4);
      var a2c$6 = a2$6.e();
      var a1$7 = a2c$6.a[idx2$2];
      var a1c$7 = a1$7.e();
      a1c$7.a[idx1$2] = elem;
      a2c$6.a[idx2$2] = a1c$7;
      return new $c_sci_Vector5(this.d, this.aj, a2c$6, this.ak, this.az, this.al, this.aA, this.am, this.a3, this.a6, this.a5, this.a4, this.f, this.h);
    } else {
      var a1$8 = this.d;
      var a1c$8 = a1$8.e();
      a1c$8.a[index] = elem;
      return new $c_sci_Vector5(a1c$8, this.aj, this.ay, this.ak, this.az, this.al, this.aA, this.am, this.a3, this.a6, this.a5, this.a4, this.f, this.h);
    }
  } else {
    throw this.aw(index);
  }
});
$p.dz = (function(elem) {
  if ((this.f.a.length < 32)) {
    var suffix1$54 = $m_sci_VectorStatics$().eO(this.f, elem);
    var length0$54 = ((1 + this.h) | 0);
    return new $c_sci_Vector5(this.d, this.aj, this.ay, this.ak, this.az, this.al, this.aA, this.am, this.a3, this.a6, this.a5, this.a4, suffix1$54, length0$54);
  } else if ((this.a4.a.length < 31)) {
    var suffix2$41 = $m_sci_VectorStatics$().z(this.a4, this.f);
    var a = new $ac_O(1);
    a.a[0] = elem;
    var length0$55 = ((1 + this.h) | 0);
    return new $c_sci_Vector5(this.d, this.aj, this.ay, this.ak, this.az, this.al, this.aA, this.am, this.a3, this.a6, this.a5, suffix2$41, a, length0$55);
  } else if ((this.a5.a.length < 31)) {
    var suffix3$29 = $m_sci_VectorStatics$().z(this.a5, $m_sci_VectorStatics$().z(this.a4, this.f));
    var a$1 = new $ac_O(1);
    a$1.a[0] = elem;
    var length0$56 = ((1 + this.h) | 0);
    return new $c_sci_Vector5(this.d, this.aj, this.ay, this.ak, this.az, this.al, this.aA, this.am, this.a3, this.a6, suffix3$29, $m_sci_VectorStatics$().bk, a$1, length0$56);
  } else if ((this.a6.a.length < 31)) {
    var suffix4$12 = $m_sci_VectorStatics$().z(this.a6, $m_sci_VectorStatics$().z(this.a5, $m_sci_VectorStatics$().z(this.a4, this.f)));
    var a$2 = new $ac_O(1);
    a$2.a[0] = elem;
    var length0$57 = ((1 + this.h) | 0);
    return new $c_sci_Vector5(this.d, this.aj, this.ay, this.ak, this.az, this.al, this.aA, this.am, this.a3, suffix4$12, $m_sci_VectorStatics$().cm, $m_sci_VectorStatics$().bk, a$2, length0$57);
  } else if ((this.a3.a.length < 30)) {
    var data5$13 = $m_sci_VectorStatics$().z(this.a3, $m_sci_VectorStatics$().z(this.a6, $m_sci_VectorStatics$().z(this.a5, $m_sci_VectorStatics$().z(this.a4, this.f))));
    var a$3 = new $ac_O(1);
    a$3.a[0] = elem;
    var length0$58 = ((1 + this.h) | 0);
    return new $c_sci_Vector5(this.d, this.aj, this.ay, this.ak, this.az, this.al, this.aA, this.am, data5$13, $m_sci_VectorStatics$().eC, $m_sci_VectorStatics$().cm, $m_sci_VectorStatics$().bk, a$3, length0$58);
  } else {
    var $x_14 = this.d;
    var $x_13 = this.aj;
    var $x_12 = this.ay;
    var $x_11 = this.ak;
    var $x_10 = this.az;
    var $x_9 = this.al;
    var $x_8 = this.aA;
    var $x_7 = this.am;
    var $x_6 = this.a3;
    var $x_5 = this.am;
    var $x_4 = $m_sci_VectorStatics$().mm;
    var x = $m_sci_VectorStatics$().z(this.a6, $m_sci_VectorStatics$().z(this.a5, $m_sci_VectorStatics$().z(this.a4, this.f)));
    var a$4 = new ($d_O.r().r().r().r().r().C)(1);
    a$4.a[0] = x;
    var $x_3 = $m_sci_VectorStatics$().eC;
    var $x_2 = $m_sci_VectorStatics$().cm;
    var $x_1 = $m_sci_VectorStatics$().bk;
    var a$5 = new $ac_O(1);
    a$5.a[0] = elem;
    return new $c_sci_Vector6($x_14, $x_13, $x_12, $x_11, $x_10, $x_9, $x_8, $x_7, $x_6, ((31457280 + $x_5) | 0), $x_4, a$4, $x_3, $x_2, $x_1, a$5, ((1 + this.h) | 0));
  }
});
$p.cx = (function() {
  return 9;
});
$p.cw = (function(idx) {
  switch (idx) {
    case 0: {
      return this.d;
      break;
    }
    case 1: {
      return this.ay;
      break;
    }
    case 2: {
      return this.az;
      break;
    }
    case 3: {
      return this.aA;
      break;
    }
    case 4: {
      return this.a3;
      break;
    }
    case 5: {
      return this.a6;
      break;
    }
    case 6: {
      return this.a5;
      break;
    }
    case 7: {
      return this.a4;
      break;
    }
    case 8: {
      return this.f;
      break;
    }
    default: {
      throw new $c_s_MatchError(idx);
    }
  }
});
$p.b = (function(v1) {
  var index = (v1 | 0);
  if (((index >= 0) && (index < this.h))) {
    var io = ((index - this.am) | 0);
    if ((io >= 0)) {
      var i5 = ((io >>> 20) | 0);
      var i4 = (31 & ((io >>> 15) | 0));
      var i3 = (31 & ((io >>> 10) | 0));
      var i2 = (31 & ((io >>> 5) | 0));
      var i1 = (31 & io);
      return ((i5 < this.a3.a.length) ? this.a3.a[i5].a[i4].a[i3].a[i2].a[i1] : ((i4 < this.a6.a.length) ? this.a6.a[i4].a[i3].a[i2].a[i1] : ((i3 < this.a5.a.length) ? this.a5.a[i3].a[i2].a[i1] : ((i2 < this.a4.a.length) ? this.a4.a[i2].a[i1] : this.f.a[i1]))));
    } else if ((index >= this.al)) {
      var io$2 = ((index - this.al) | 0);
      return this.aA.a[((io$2 >>> 15) | 0)].a[(31 & ((io$2 >>> 10) | 0))].a[(31 & ((io$2 >>> 5) | 0))].a[(31 & io$2)];
    } else if ((index >= this.ak)) {
      var io$3 = ((index - this.ak) | 0);
      return this.az.a[((io$3 >>> 10) | 0)].a[(31 & ((io$3 >>> 5) | 0))].a[(31 & io$3)];
    } else if ((index >= this.aj)) {
      var io$4 = ((index - this.aj) | 0);
      return this.ay.a[((io$4 >>> 5) | 0)].a[(31 & io$4)];
    } else {
      return this.d.a[index];
    }
  } else {
    throw this.aw(index);
  }
});
var $d_sci_Vector5 = new $TypeData().i($c_sci_Vector5, "scala.collection.immutable.Vector5", ({
  gu: 1,
  ae: 1,
  ag: 1,
  a6: 1,
  x: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  r: 1,
  w: 1,
  v: 1,
  p: 1,
  o: 1,
  C: 1,
  y: 1,
  k: 1,
  q: 1,
  z: 1,
  a: 1,
  U: 1
}));
/** @constructor */
function $c_sci_Vector6(_prefix1, len1, prefix2, len12, prefix3, len123, prefix4, len1234, prefix5, len12345, data6, suffix5, suffix4, suffix3, suffix2, _suffix1, _length0) {
  this.d = null;
  this.f = null;
  this.h = 0;
  this.a7 = 0;
  this.an = null;
  this.a8 = 0;
  this.ao = null;
  this.a9 = 0;
  this.ap = null;
  this.aa = 0;
  this.aq = null;
  this.af = 0;
  this.U = null;
  this.Y = null;
  this.X = null;
  this.W = null;
  this.V = null;
  this.a7 = len1;
  this.an = prefix2;
  this.a8 = len12;
  this.ao = prefix3;
  this.a9 = len123;
  this.ap = prefix4;
  this.aa = len1234;
  this.aq = prefix5;
  this.af = len12345;
  this.U = data6;
  this.Y = suffix5;
  this.X = suffix4;
  this.W = suffix3;
  this.V = suffix2;
  $ct_sci_BigVector__AO__AO__I__(this, _prefix1, _suffix1, _length0);
}
$p = $c_sci_Vector6.prototype = new $h_sci_BigVector();
$p.constructor = $c_sci_Vector6;
/** @constructor */
function $h_sci_Vector6() {
}
$h_sci_Vector6.prototype = $p;
$p.v = (function(index) {
  if (((index >= 0) && (index < this.h))) {
    var io = ((index - this.af) | 0);
    if ((io >= 0)) {
      var i6 = ((io >>> 25) | 0);
      var i5 = (31 & ((io >>> 20) | 0));
      var i4 = (31 & ((io >>> 15) | 0));
      var i3 = (31 & ((io >>> 10) | 0));
      var i2 = (31 & ((io >>> 5) | 0));
      var i1 = (31 & io);
      return ((i6 < this.U.a.length) ? this.U.a[i6].a[i5].a[i4].a[i3].a[i2].a[i1] : ((i5 < this.Y.a.length) ? this.Y.a[i5].a[i4].a[i3].a[i2].a[i1] : ((i4 < this.X.a.length) ? this.X.a[i4].a[i3].a[i2].a[i1] : ((i3 < this.W.a.length) ? this.W.a[i3].a[i2].a[i1] : ((i2 < this.V.a.length) ? this.V.a[i2].a[i1] : this.f.a[i1])))));
    } else if ((index >= this.aa)) {
      var io$2 = ((index - this.aa) | 0);
      return this.aq.a[((io$2 >>> 20) | 0)].a[(31 & ((io$2 >>> 15) | 0))].a[(31 & ((io$2 >>> 10) | 0))].a[(31 & ((io$2 >>> 5) | 0))].a[(31 & io$2)];
    } else if ((index >= this.a9)) {
      var io$3 = ((index - this.a9) | 0);
      return this.ap.a[((io$3 >>> 15) | 0)].a[(31 & ((io$3 >>> 10) | 0))].a[(31 & ((io$3 >>> 5) | 0))].a[(31 & io$3)];
    } else if ((index >= this.a8)) {
      var io$4 = ((index - this.a8) | 0);
      return this.ao.a[((io$4 >>> 10) | 0)].a[(31 & ((io$4 >>> 5) | 0))].a[(31 & io$4)];
    } else if ((index >= this.a7)) {
      var io$5 = ((index - this.a7) | 0);
      return this.an.a[((io$5 >>> 5) | 0)].a[(31 & io$5)];
    } else {
      return this.d.a[index];
    }
  } else {
    throw this.aw(index);
  }
});
$p.dG = (function(index, elem) {
  if (((index >= 0) && (index < this.h))) {
    if ((index >= this.af)) {
      var io = ((index - this.af) | 0);
      var i6 = ((io >>> 25) | 0);
      var i5 = (31 & ((io >>> 20) | 0));
      var i4 = (31 & ((io >>> 15) | 0));
      var i3 = (31 & ((io >>> 10) | 0));
      var i2 = (31 & ((io >>> 5) | 0));
      var i1 = (31 & io);
      if ((i6 < this.U.a.length)) {
        var a6 = this.U;
        var a6c = a6.e();
        var a5 = a6c.a[i6];
        var a5c = a5.e();
        var a4 = a5c.a[i5];
        var a4c = a4.e();
        var a3 = a4c.a[i4];
        var a3c = a3.e();
        var a2 = a3c.a[i3];
        var a2c = a2.e();
        var a1 = a2c.a[i2];
        var a1c = a1.e();
        a1c.a[i1] = elem;
        a2c.a[i2] = a1c;
        a3c.a[i3] = a2c;
        a4c.a[i4] = a3c;
        a5c.a[i5] = a4c;
        a6c.a[i6] = a5c;
        return new $c_sci_Vector6(this.d, this.a7, this.an, this.a8, this.ao, this.a9, this.ap, this.aa, this.aq, this.af, a6c, this.Y, this.X, this.W, this.V, this.f, this.h);
      } else if ((i5 < this.Y.a.length)) {
        var a5$1 = this.Y;
        var a5c$1 = a5$1.e();
        var a4$1 = a5c$1.a[i5];
        var a4c$1 = a4$1.e();
        var a3$1 = a4c$1.a[i4];
        var a3c$1 = a3$1.e();
        var a2$1 = a3c$1.a[i3];
        var a2c$1 = a2$1.e();
        var a1$1 = a2c$1.a[i2];
        var a1c$1 = a1$1.e();
        a1c$1.a[i1] = elem;
        a2c$1.a[i2] = a1c$1;
        a3c$1.a[i3] = a2c$1;
        a4c$1.a[i4] = a3c$1;
        a5c$1.a[i5] = a4c$1;
        return new $c_sci_Vector6(this.d, this.a7, this.an, this.a8, this.ao, this.a9, this.ap, this.aa, this.aq, this.af, this.U, a5c$1, this.X, this.W, this.V, this.f, this.h);
      } else if ((i4 < this.X.a.length)) {
        var a4$2 = this.X;
        var a4c$2 = a4$2.e();
        var a3$2 = a4c$2.a[i4];
        var a3c$2 = a3$2.e();
        var a2$2 = a3c$2.a[i3];
        var a2c$2 = a2$2.e();
        var a1$2 = a2c$2.a[i2];
        var a1c$2 = a1$2.e();
        a1c$2.a[i1] = elem;
        a2c$2.a[i2] = a1c$2;
        a3c$2.a[i3] = a2c$2;
        a4c$2.a[i4] = a3c$2;
        return new $c_sci_Vector6(this.d, this.a7, this.an, this.a8, this.ao, this.a9, this.ap, this.aa, this.aq, this.af, this.U, this.Y, a4c$2, this.W, this.V, this.f, this.h);
      } else if ((i3 < this.W.a.length)) {
        var a3$3 = this.W;
        var a3c$3 = a3$3.e();
        var a2$3 = a3c$3.a[i3];
        var a2c$3 = a2$3.e();
        var a1$3 = a2c$3.a[i2];
        var a1c$3 = a1$3.e();
        a1c$3.a[i1] = elem;
        a2c$3.a[i2] = a1c$3;
        a3c$3.a[i3] = a2c$3;
        return new $c_sci_Vector6(this.d, this.a7, this.an, this.a8, this.ao, this.a9, this.ap, this.aa, this.aq, this.af, this.U, this.Y, this.X, a3c$3, this.V, this.f, this.h);
      } else if ((i2 < this.V.a.length)) {
        var a2$4 = this.V;
        var a2c$4 = a2$4.e();
        var a1$4 = a2c$4.a[i2];
        var a1c$4 = a1$4.e();
        a1c$4.a[i1] = elem;
        a2c$4.a[i2] = a1c$4;
        return new $c_sci_Vector6(this.d, this.a7, this.an, this.a8, this.ao, this.a9, this.ap, this.aa, this.aq, this.af, this.U, this.Y, this.X, this.W, a2c$4, this.f, this.h);
      } else {
        var a1$5 = this.f;
        var a1c$5 = a1$5.e();
        a1c$5.a[i1] = elem;
        return new $c_sci_Vector6(this.d, this.a7, this.an, this.a8, this.ao, this.a9, this.ap, this.aa, this.aq, this.af, this.U, this.Y, this.X, this.W, this.V, a1c$5, this.h);
      }
    } else if ((index >= this.aa)) {
      var io$2 = ((index - this.aa) | 0);
      var a5$2 = this.aq;
      var idx5 = ((io$2 >>> 20) | 0);
      var idx4 = (31 & ((io$2 >>> 15) | 0));
      var idx3 = (31 & ((io$2 >>> 10) | 0));
      var idx2 = (31 & ((io$2 >>> 5) | 0));
      var idx1 = (31 & io$2);
      var a5c$2 = a5$2.e();
      var a4$3 = a5c$2.a[idx5];
      var a4c$3 = a4$3.e();
      var a3$4 = a4c$3.a[idx4];
      var a3c$4 = a3$4.e();
      var a2$5 = a3c$4.a[idx3];
      var a2c$5 = a2$5.e();
      var a1$6 = a2c$5.a[idx2];
      var a1c$6 = a1$6.e();
      a1c$6.a[idx1] = elem;
      a2c$5.a[idx2] = a1c$6;
      a3c$4.a[idx3] = a2c$5;
      a4c$3.a[idx4] = a3c$4;
      a5c$2.a[idx5] = a4c$3;
      return new $c_sci_Vector6(this.d, this.a7, this.an, this.a8, this.ao, this.a9, this.ap, this.aa, a5c$2, this.af, this.U, this.Y, this.X, this.W, this.V, this.f, this.h);
    } else if ((index >= this.a9)) {
      var io$3 = ((index - this.a9) | 0);
      var a4$4 = this.ap;
      var idx4$1 = ((io$3 >>> 15) | 0);
      var idx3$1 = (31 & ((io$3 >>> 10) | 0));
      var idx2$1 = (31 & ((io$3 >>> 5) | 0));
      var idx1$1 = (31 & io$3);
      var a4c$4 = a4$4.e();
      var a3$5 = a4c$4.a[idx4$1];
      var a3c$5 = a3$5.e();
      var a2$6 = a3c$5.a[idx3$1];
      var a2c$6 = a2$6.e();
      var a1$7 = a2c$6.a[idx2$1];
      var a1c$7 = a1$7.e();
      a1c$7.a[idx1$1] = elem;
      a2c$6.a[idx2$1] = a1c$7;
      a3c$5.a[idx3$1] = a2c$6;
      a4c$4.a[idx4$1] = a3c$5;
      return new $c_sci_Vector6(this.d, this.a7, this.an, this.a8, this.ao, this.a9, a4c$4, this.aa, this.aq, this.af, this.U, this.Y, this.X, this.W, this.V, this.f, this.h);
    } else if ((index >= this.a8)) {
      var io$4 = ((index - this.a8) | 0);
      var a3$6 = this.ao;
      var idx3$2 = ((io$4 >>> 10) | 0);
      var idx2$2 = (31 & ((io$4 >>> 5) | 0));
      var idx1$2 = (31 & io$4);
      var a3c$6 = a3$6.e();
      var a2$7 = a3c$6.a[idx3$2];
      var a2c$7 = a2$7.e();
      var a1$8 = a2c$7.a[idx2$2];
      var a1c$8 = a1$8.e();
      a1c$8.a[idx1$2] = elem;
      a2c$7.a[idx2$2] = a1c$8;
      a3c$6.a[idx3$2] = a2c$7;
      return new $c_sci_Vector6(this.d, this.a7, this.an, this.a8, a3c$6, this.a9, this.ap, this.aa, this.aq, this.af, this.U, this.Y, this.X, this.W, this.V, this.f, this.h);
    } else if ((index >= this.a7)) {
      var io$5 = ((index - this.a7) | 0);
      var a2$8 = this.an;
      var idx2$3 = ((io$5 >>> 5) | 0);
      var idx1$3 = (31 & io$5);
      var a2c$8 = a2$8.e();
      var a1$9 = a2c$8.a[idx2$3];
      var a1c$9 = a1$9.e();
      a1c$9.a[idx1$3] = elem;
      a2c$8.a[idx2$3] = a1c$9;
      return new $c_sci_Vector6(this.d, this.a7, a2c$8, this.a8, this.ao, this.a9, this.ap, this.aa, this.aq, this.af, this.U, this.Y, this.X, this.W, this.V, this.f, this.h);
    } else {
      var a1$10 = this.d;
      var a1c$10 = a1$10.e();
      a1c$10.a[index] = elem;
      return new $c_sci_Vector6(a1c$10, this.a7, this.an, this.a8, this.ao, this.a9, this.ap, this.aa, this.aq, this.af, this.U, this.Y, this.X, this.W, this.V, this.f, this.h);
    }
  } else {
    throw this.aw(index);
  }
});
$p.dz = (function(elem) {
  if ((this.f.a.length < 32)) {
    var suffix1$79 = $m_sci_VectorStatics$().eO(this.f, elem);
    var length0$79 = ((1 + this.h) | 0);
    return new $c_sci_Vector6(this.d, this.a7, this.an, this.a8, this.ao, this.a9, this.ap, this.aa, this.aq, this.af, this.U, this.Y, this.X, this.W, this.V, suffix1$79, length0$79);
  } else if ((this.V.a.length < 31)) {
    var suffix2$63 = $m_sci_VectorStatics$().z(this.V, this.f);
    var a = new $ac_O(1);
    a.a[0] = elem;
    var length0$80 = ((1 + this.h) | 0);
    return new $c_sci_Vector6(this.d, this.a7, this.an, this.a8, this.ao, this.a9, this.ap, this.aa, this.aq, this.af, this.U, this.Y, this.X, this.W, suffix2$63, a, length0$80);
  } else if ((this.W.a.length < 31)) {
    var suffix3$52 = $m_sci_VectorStatics$().z(this.W, $m_sci_VectorStatics$().z(this.V, this.f));
    var a$1 = new $ac_O(1);
    a$1.a[0] = elem;
    var length0$81 = ((1 + this.h) | 0);
    return new $c_sci_Vector6(this.d, this.a7, this.an, this.a8, this.ao, this.a9, this.ap, this.aa, this.aq, this.af, this.U, this.Y, this.X, suffix3$52, $m_sci_VectorStatics$().bk, a$1, length0$81);
  } else if ((this.X.a.length < 31)) {
    var suffix4$36 = $m_sci_VectorStatics$().z(this.X, $m_sci_VectorStatics$().z(this.W, $m_sci_VectorStatics$().z(this.V, this.f)));
    var a$2 = new $ac_O(1);
    a$2.a[0] = elem;
    var length0$82 = ((1 + this.h) | 0);
    return new $c_sci_Vector6(this.d, this.a7, this.an, this.a8, this.ao, this.a9, this.ap, this.aa, this.aq, this.af, this.U, this.Y, suffix4$36, $m_sci_VectorStatics$().cm, $m_sci_VectorStatics$().bk, a$2, length0$82);
  } else if ((this.Y.a.length < 31)) {
    var suffix5$15 = $m_sci_VectorStatics$().z(this.Y, $m_sci_VectorStatics$().z(this.X, $m_sci_VectorStatics$().z(this.W, $m_sci_VectorStatics$().z(this.V, this.f))));
    var a$3 = new $ac_O(1);
    a$3.a[0] = elem;
    var length0$83 = ((1 + this.h) | 0);
    return new $c_sci_Vector6(this.d, this.a7, this.an, this.a8, this.ao, this.a9, this.ap, this.aa, this.aq, this.af, this.U, suffix5$15, $m_sci_VectorStatics$().eC, $m_sci_VectorStatics$().cm, $m_sci_VectorStatics$().bk, a$3, length0$83);
  } else if ((this.U.a.length < 62)) {
    var data6$16 = $m_sci_VectorStatics$().z(this.U, $m_sci_VectorStatics$().z(this.Y, $m_sci_VectorStatics$().z(this.X, $m_sci_VectorStatics$().z(this.W, $m_sci_VectorStatics$().z(this.V, this.f)))));
    var a$4 = new $ac_O(1);
    a$4.a[0] = elem;
    var length0$84 = ((1 + this.h) | 0);
    return new $c_sci_Vector6(this.d, this.a7, this.an, this.a8, this.ao, this.a9, this.ap, this.aa, this.aq, this.af, data6$16, $m_sci_VectorStatics$().iq, $m_sci_VectorStatics$().eC, $m_sci_VectorStatics$().cm, $m_sci_VectorStatics$().bk, a$4, length0$84);
  } else {
    throw $ct_jl_IllegalArgumentException__(new $c_jl_IllegalArgumentException());
  }
});
$p.cx = (function() {
  return 11;
});
$p.cw = (function(idx) {
  switch (idx) {
    case 0: {
      return this.d;
      break;
    }
    case 1: {
      return this.an;
      break;
    }
    case 2: {
      return this.ao;
      break;
    }
    case 3: {
      return this.ap;
      break;
    }
    case 4: {
      return this.aq;
      break;
    }
    case 5: {
      return this.U;
      break;
    }
    case 6: {
      return this.Y;
      break;
    }
    case 7: {
      return this.X;
      break;
    }
    case 8: {
      return this.W;
      break;
    }
    case 9: {
      return this.V;
      break;
    }
    case 10: {
      return this.f;
      break;
    }
    default: {
      throw new $c_s_MatchError(idx);
    }
  }
});
$p.b = (function(v1) {
  var index = (v1 | 0);
  if (((index >= 0) && (index < this.h))) {
    var io = ((index - this.af) | 0);
    if ((io >= 0)) {
      var i6 = ((io >>> 25) | 0);
      var i5 = (31 & ((io >>> 20) | 0));
      var i4 = (31 & ((io >>> 15) | 0));
      var i3 = (31 & ((io >>> 10) | 0));
      var i2 = (31 & ((io >>> 5) | 0));
      var i1 = (31 & io);
      return ((i6 < this.U.a.length) ? this.U.a[i6].a[i5].a[i4].a[i3].a[i2].a[i1] : ((i5 < this.Y.a.length) ? this.Y.a[i5].a[i4].a[i3].a[i2].a[i1] : ((i4 < this.X.a.length) ? this.X.a[i4].a[i3].a[i2].a[i1] : ((i3 < this.W.a.length) ? this.W.a[i3].a[i2].a[i1] : ((i2 < this.V.a.length) ? this.V.a[i2].a[i1] : this.f.a[i1])))));
    } else if ((index >= this.aa)) {
      var io$2 = ((index - this.aa) | 0);
      return this.aq.a[((io$2 >>> 20) | 0)].a[(31 & ((io$2 >>> 15) | 0))].a[(31 & ((io$2 >>> 10) | 0))].a[(31 & ((io$2 >>> 5) | 0))].a[(31 & io$2)];
    } else if ((index >= this.a9)) {
      var io$3 = ((index - this.a9) | 0);
      return this.ap.a[((io$3 >>> 15) | 0)].a[(31 & ((io$3 >>> 10) | 0))].a[(31 & ((io$3 >>> 5) | 0))].a[(31 & io$3)];
    } else if ((index >= this.a8)) {
      var io$4 = ((index - this.a8) | 0);
      return this.ao.a[((io$4 >>> 10) | 0)].a[(31 & ((io$4 >>> 5) | 0))].a[(31 & io$4)];
    } else if ((index >= this.a7)) {
      var io$5 = ((index - this.a7) | 0);
      return this.an.a[((io$5 >>> 5) | 0)].a[(31 & io$5)];
    } else {
      return this.d.a[index];
    }
  } else {
    throw this.aw(index);
  }
});
var $d_sci_Vector6 = new $TypeData().i($c_sci_Vector6, "scala.collection.immutable.Vector6", ({
  gv: 1,
  ae: 1,
  ag: 1,
  a6: 1,
  x: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  r: 1,
  w: 1,
  v: 1,
  p: 1,
  o: 1,
  C: 1,
  y: 1,
  k: 1,
  q: 1,
  z: 1,
  a: 1,
  U: 1
}));
function $ct_scm_StringBuilder__jl_StringBuilder__($thiz, underlying) {
  $thiz.aM = underlying;
  return $thiz;
}
function $ct_scm_StringBuilder__($thiz) {
  $ct_scm_StringBuilder__jl_StringBuilder__($thiz, $ct_jl_StringBuilder__(new $c_jl_StringBuilder()));
  return $thiz;
}
/** @constructor */
function $c_scm_StringBuilder() {
  this.aM = null;
}
$p = $c_scm_StringBuilder.prototype = new $h_scm_AbstractSeq();
$p.constructor = $c_scm_StringBuilder;
/** @constructor */
function $h_scm_StringBuilder() {
}
$h_scm_StringBuilder.prototype = $p;
$p.aU = (function(elems) {
  return $f_scm_Growable__addAll__sc_IterableOnce__scm_Growable(this, elems);
});
$p.aX = (function(size) {
});
$p.i = (function() {
  return $ct_sc_IndexedSeqView$IndexedSeqViewIterator__sc_IndexedSeqView__(new $c_sc_IndexedSeqView$IndexedSeqViewIterator(), new $c_sc_IndexedSeqView$Id(this));
});
$p.bc = (function(len) {
  var x = this.aM.q();
  return ((x === len) ? 0 : ((x < len) ? (-1) : 1));
});
$p.bq = (function() {
  return "IndexedSeq";
});
$p.q = (function() {
  return this.aM.q();
});
$p.x = (function() {
  return this.aM.q();
});
$p.oX = (function(x) {
  var this$1 = this.aM;
  var str = ("" + $cToS(x));
  this$1.p = (this$1.p + str);
  return this;
});
$p.t = (function() {
  return this.aM.p;
});
$p.n5 = (function(xs) {
  if (false) {
    var this$3 = this.aM;
    var str = xs.rL;
    this$3.p = (("" + this$3.p) + str);
  } else if ((xs instanceof $c_scm_ArraySeq$ofChar)) {
    this.aM.n4(xs.bH);
  } else if ((xs instanceof $c_scm_StringBuilder)) {
    var this$4 = this.aM;
    var s = xs.aM;
    this$4.p = (("" + this$4.p) + s);
  } else {
    var ks = xs.x();
    if ((ks !== 0)) {
      var b = this.aM;
      if ((ks > 0)) {
        b.q();
      }
      var it = xs.i();
      while (it.m()) {
        var c = $uC(it.g());
        var str$1 = ("" + $cToS(c));
        b.p = (b.p + str$1);
      }
    }
  }
  return this;
});
$p.c = (function() {
  return (this.aM.q() === 0);
});
$p.v = (function(i) {
  return $bC(this.aM.nc(i));
});
$p.b = (function(v1) {
  var i = (v1 | 0);
  return $bC(this.aM.nc(i));
});
$p.eR = (function(coll) {
  return $ct_scm_StringBuilder__(new $c_scm_StringBuilder()).n5(coll);
});
$p.g2 = (function(coll) {
  return $ct_scm_StringBuilder__(new $c_scm_StringBuilder()).n5(coll);
});
$p.aV = (function(elem) {
  return this.oX($uC(elem));
});
$p.b2 = (function() {
  return this.aM.p;
});
$p.bn = (function() {
  return $m_scm_IndexedSeq$();
});
function $isArrayOf_scm_StringBuilder(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.cp)));
}
var $d_scm_StringBuilder = new $TypeData().i($c_scm_StringBuilder, "scala.collection.mutable.StringBuilder", ({
  cp: 1,
  L: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  J: 1,
  A: 1,
  H: 1,
  O: 1,
  N: 1,
  G: 1,
  I: 1,
  M: 1,
  a7: 1,
  p: 1,
  o: 1,
  S: 1,
  R: 1,
  aD: 1,
  a: 1
}));
function $isArrayOf_scm_LinkedHashMap(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.gU)));
}
function $p_scm_ListBuffer__copyElems__V($thiz) {
  var buf = new $c_scm_ListBuffer().hl($thiz);
  $thiz.bV = buf.bV;
  $thiz.cR = buf.cR;
  $thiz.gM = false;
}
function $p_scm_ListBuffer__ensureUnaliased__V($thiz) {
  $thiz.gN = ((1 + $thiz.gN) | 0);
  if ($thiz.gM) {
    $p_scm_ListBuffer__copyElems__V($thiz);
  }
}
/** @constructor */
function $c_scm_ListBuffer() {
  this.gN = 0;
  this.bV = null;
  this.cR = null;
  this.gM = false;
  this.bW = 0;
  this.gN = 0;
  this.bV = $m_sci_Nil$();
  this.cR = null;
  this.gM = false;
  this.bW = 0;
}
$p = $c_scm_ListBuffer.prototype = new $h_scm_AbstractBuffer();
$p.constructor = $c_scm_ListBuffer;
/** @constructor */
function $h_scm_ListBuffer() {
}
$h_scm_ListBuffer.prototype = $p;
$p.cq = (function(f) {
  return $f_sc_StrictOptimizedSeqOps__distinctBy__F1__O(this, f);
});
$p.aX = (function(size) {
});
$p.i = (function() {
  return new $c_scm_MutationTracker$CheckedIterator(this.bV.i(), new $c_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c((() => this.gN)));
});
$p.dD = (function() {
  return $m_scm_ListBuffer$();
});
$p.v = (function(i) {
  return $f_sc_LinearSeqOps__apply__I__O(this.bV, i);
});
$p.q = (function() {
  return this.bW;
});
$p.x = (function() {
  return this.bW;
});
$p.c = (function() {
  return (this.bW === 0);
});
$p.oh = (function() {
  this.gM = (!this.c());
  return this.bV;
});
$p.p5 = (function(elem) {
  $p_scm_ListBuffer__ensureUnaliased__V(this);
  var last1 = new $c_sci_$colon$colon(elem, $m_sci_Nil$());
  if ((this.bW === 0)) {
    this.bV = last1;
  } else {
    var x$proxy2 = this.cR;
    if ((x$proxy2 === null)) {
      $m_sr_Scala3RunTime$().bp();
    }
    x$proxy2.J = last1;
  }
  this.cR = last1;
  this.bW = ((1 + this.bW) | 0);
  return this;
});
$p.hl = (function(xs) {
  var it = xs.i();
  if (it.m()) {
    var len = 1;
    var last0 = new $c_sci_$colon$colon(it.g(), $m_sci_Nil$());
    this.bV = last0;
    while (it.m()) {
      var last1 = new $c_sci_$colon$colon(it.g(), $m_sci_Nil$());
      last0.J = last1;
      last0 = last1;
      len = ((1 + len) | 0);
    }
    this.bW = len;
    this.cR = last0;
  }
  return this;
});
$p.oV = (function(xs) {
  var it = xs.i();
  if (it.m()) {
    var fresh = new $c_scm_ListBuffer().hl(it);
    $p_scm_ListBuffer__ensureUnaliased__V(this);
    if ((this.bW === 0)) {
      this.bV = fresh.bV;
    } else {
      var x$proxy3 = this.cR;
      if ((x$proxy3 === null)) {
        $m_sr_Scala3RunTime$().bp();
      }
      x$proxy3.J = fresh.bV;
    }
    this.cR = fresh.cR;
    this.bW = ((this.bW + fresh.bW) | 0);
  }
  return this;
});
$p.bq = (function() {
  return "ListBuffer";
});
$p.bn = (function() {
  return $m_scm_ListBuffer$();
});
$p.b = (function(v1) {
  var i = (v1 | 0);
  return $f_sc_LinearSeqOps__apply__I__O(this.bV, i);
});
$p.b2 = (function() {
  return this.oh();
});
$p.aV = (function(elem) {
  return this.p5(elem);
});
$p.aU = (function(elems) {
  return this.oV(elems);
});
function $isArrayOf_scm_ListBuffer(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.co)));
}
var $d_scm_ListBuffer = new $TypeData().i($c_scm_ListBuffer, "scala.collection.mutable.ListBuffer", ({
  co: 1,
  aS: 1,
  L: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  J: 1,
  A: 1,
  H: 1,
  O: 1,
  N: 1,
  G: 1,
  I: 1,
  au: 1,
  aT: 1,
  k: 1,
  q: 1,
  M: 1,
  a7: 1,
  a: 1,
  U: 1
}));
function $ct_scm_ArrayBuffer__AO__I__($thiz, initialElements, initialSize) {
  $thiz.eD = 0;
  $thiz.cN = initialElements;
  $thiz.aT = initialSize;
  return $thiz;
}
function $ct_scm_ArrayBuffer__($thiz) {
  $ct_scm_ArrayBuffer__AO__I__($thiz, new $ac_O(16), 0);
  return $thiz;
}
/** @constructor */
function $c_scm_ArrayBuffer() {
  this.eD = 0;
  this.cN = null;
  this.aT = 0;
}
$p = $c_scm_ArrayBuffer.prototype = new $h_scm_AbstractBuffer();
$p.constructor = $c_scm_ArrayBuffer;
/** @constructor */
function $h_scm_ArrayBuffer() {
}
$h_scm_ArrayBuffer.prototype = $p;
$p.i = (function() {
  return this.rI().i();
});
$p.bc = (function(len) {
  var x = this.aT;
  return ((x === len) ? 0 : ((x < len) ? (-1) : 1));
});
$p.cq = (function(f) {
  return $f_sc_StrictOptimizedSeqOps__distinctBy__F1__O(this, f);
});
$p.x = (function() {
  return this.aT;
});
$p.iT = (function(n) {
  this.cN = $m_scm_ArrayBuffer$().oa(this.cN, this.aT, n);
});
$p.aX = (function(size) {
  if (((size > this.aT) && (size >= 1))) {
    this.iT(size);
  }
});
$p.v = (function(n) {
  var hi = ((1 + n) | 0);
  if ((n < 0)) {
    throw $m_scg_CommonErrors$().ja(n, ((this.aT - 1) | 0));
  }
  if ((hi > this.aT)) {
    throw $m_scg_CommonErrors$().ja(((hi - 1) | 0), ((this.aT - 1) | 0));
  }
  return this.cN.a[n];
});
$p.q = (function() {
  return this.aT;
});
$p.rI = (function() {
  return new $c_scm_ArrayBufferView(this, new $c_sr_AbstractFunction0_$$Lambda$07eded5776954a9c145e92c329afd52873ad179c((() => this.eD)));
});
$p.dD = (function() {
  return $m_scm_ArrayBuffer$();
});
$p.p2 = (function(elem) {
  this.eD = ((1 + this.eD) | 0);
  var newSize = ((1 + this.aT) | 0);
  if ((this.cN.a.length <= ((newSize - 1) | 0))) {
    this.iT(newSize);
  }
  this.aT = newSize;
  this.cN.a[((newSize - 1) | 0)] = elem;
  return this;
});
$p.n0 = (function(elems) {
  if ((elems instanceof $c_scm_ArrayBuffer)) {
    var elemsLength = elems.aT;
    if ((elemsLength > 0)) {
      this.eD = ((1 + this.eD) | 0);
      this.iT(((this.aT + elemsLength) | 0));
      $m_s_Array$().fZ(elems.cN, 0, this.cN, this.aT, elemsLength);
      this.aT = ((this.aT + elemsLength) | 0);
    }
  } else {
    $f_scm_Growable__addAll__sc_IterableOnce__scm_Growable(this, elems);
  }
  return this;
});
$p.bq = (function() {
  return "ArrayBuffer";
});
$p.bI = (function(xs, start, len) {
  var srcLen = this.aT;
  var destLen = $m_jl_reflect_Array$().bJ(xs);
  var limit = ((len < srcLen) ? len : srcLen);
  var capacity = ((start < 0) ? destLen : ((destLen - start) | 0));
  var total = ((capacity < limit) ? capacity : limit);
  var copied = ((total < 0) ? 0 : total);
  if ((copied > 0)) {
    $m_s_Array$().fZ(this.cN, 0, xs, start, copied);
  }
  return copied;
});
$p.b = (function(v1) {
  return this.v((v1 | 0));
});
$p.bn = (function() {
  return $m_scm_ArrayBuffer$();
});
$p.aV = (function(elem) {
  return this.p2(elem);
});
$p.aU = (function(elems) {
  return this.n0(elems);
});
function $isArrayOf_scm_ArrayBuffer(obj, depth) {
  return (!(!(((obj && obj.$classData) && (obj.$classData.D === depth)) && obj.$classData.B.n.cb)));
}
var $d_scm_ArrayBuffer = new $TypeData().i($c_scm_ArrayBuffer, "scala.collection.mutable.ArrayBuffer", ({
  cb: 1,
  aS: 1,
  L: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  J: 1,
  A: 1,
  H: 1,
  O: 1,
  N: 1,
  G: 1,
  I: 1,
  au: 1,
  aT: 1,
  p: 1,
  o: 1,
  S: 1,
  R: 1,
  cn: 1,
  k: 1,
  q: 1,
  a: 1,
  U: 1
}));
function $ct_sjs_js_WrappedArray__sjs_js_Array__($thiz, array) {
  $thiz.dw = array;
  return $thiz;
}
function $ct_sjs_js_WrappedArray__($thiz) {
  $ct_sjs_js_WrappedArray__sjs_js_Array__($thiz, []);
  return $thiz;
}
/** @constructor */
function $c_sjs_js_WrappedArray() {
  this.dw = null;
}
$p = $c_sjs_js_WrappedArray.prototype = new $h_scm_AbstractBuffer();
$p.constructor = $c_sjs_js_WrappedArray;
/** @constructor */
function $h_sjs_js_WrappedArray() {
}
$h_sjs_js_WrappedArray.prototype = $p;
$p.aX = (function(size) {
});
$p.bq = (function() {
  return "IndexedSeq";
});
$p.i = (function() {
  return $ct_sc_IndexedSeqView$IndexedSeqViewIterator__sc_IndexedSeqView__(new $c_sc_IndexedSeqView$IndexedSeqViewIterator(), new $c_sc_IndexedSeqView$Id(this));
});
$p.bc = (function(len) {
  var x = (this.dw.length | 0);
  return ((x === len) ? 0 : ((x < len) ? (-1) : 1));
});
$p.cq = (function(f) {
  return $f_sc_StrictOptimizedSeqOps__distinctBy__F1__O(this, f);
});
$p.dD = (function() {
  return $m_sjs_js_WrappedArray$();
});
$p.v = (function(index) {
  return this.dw[index];
});
$p.q = (function() {
  return (this.dw.length | 0);
});
$p.x = (function() {
  return (this.dw.length | 0);
});
$p.bZ = (function() {
  return "WrappedArray";
});
$p.b2 = (function() {
  return this;
});
$p.aV = (function(elem) {
  this.dw.push(elem);
  return this;
});
$p.b = (function(v1) {
  var index = (v1 | 0);
  return this.dw[index];
});
$p.bn = (function() {
  return $m_sjs_js_WrappedArray$();
});
var $d_sjs_js_WrappedArray = new $TypeData().i($c_sjs_js_WrappedArray, "scala.scalajs.js.WrappedArray", ({
  i4: 1,
  aS: 1,
  L: 1,
  n: 1,
  i: 1,
  b: 1,
  c: 1,
  h: 1,
  g: 1,
  f: 1,
  e: 1,
  j: 1,
  l: 1,
  d: 1,
  m: 1,
  J: 1,
  A: 1,
  H: 1,
  O: 1,
  N: 1,
  G: 1,
  I: 1,
  au: 1,
  aT: 1,
  q: 1,
  k: 1,
  R: 1,
  p: 1,
  o: 1,
  S: 1,
  cn: 1,
  M: 1,
  a: 1
}));
$s_Ldpm_Main__main__AT__V(new ($d_T.r().C)([]));
