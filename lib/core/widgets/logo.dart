import 'package:cyper_shield_jo/core/utils/reponsive_size_helper.dart';
import 'package:flutter/material.dart';

class Logo extends StatelessWidget {
  const Logo({super.key});

  @override
  Widget build(BuildContext context) {
    return Image.asset(
      'assets/images/CyperShield_logo.png',
      height: responsiveHeight(context, 300),
      width: responsiveWidth(context, 300),
    );
  }
}
