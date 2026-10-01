import 'package:cyper_shield_jo/core/constants/app_colors.dart';
import 'package:cyper_shield_jo/core/utils/reponsive_size_helper.dart';
import 'package:flutter/material.dart';

class buildTopBar extends StatelessWidget {
  const buildTopBar({super.key});

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    double titleFont = screenWidth < 600 ? 25 : 20;
    double paddingValue = screenWidth < 600 ? 8 : 15;
    return Padding(
      padding: EdgeInsets.all(paddingValue),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            children: [
              Padding(
                padding: const EdgeInsets.all(15.0),
                child: Container(
                  width: responsiveWidth(context, 50),
                  height: responsiveHeight(context, 50),
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      colors: [
                        AppColors.primaryColor,
                        AppColors.seconderyColor,
                      ],
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                    ),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: const Icon(
                    Icons.shield_rounded,
                    color: Colors.white,
                    size: 22,
                  ),
                ),
              ),
              SizedBox(width: responsiveWidth(context, 12)),
              Column(
                children: [
                  Text(
                    "Aman_Jo",
                    style: TextStyle(
                      color: AppColors.whiteColor,
                      fontSize: titleFont,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Text(
                    "ThreatDetector",
                    style: TextStyle(
                      color: AppColors.seconderyColor,
                      fontSize: 12,
                    ),
                  ),
                ],
              ),
            ],
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: IconButton(
              onPressed: () {},
              icon: Icon(Icons.language, size: 30),
            ),
          ),
        ],
      ),
    );
  }
}
