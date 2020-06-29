import 'package:flutter/material.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';

class Loader extends StatelessWidget {
  const Loader({this.size = 250, this.color = Colors.black});

  /// The size of the loader
  final double size;

  /// The color of the loader
  final Color color;

  @override
  Widget build(BuildContext context) => SpinKitWave(
        color: color,
        size: size,
      );
}
