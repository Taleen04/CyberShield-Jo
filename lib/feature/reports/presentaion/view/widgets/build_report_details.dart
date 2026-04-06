import 'package:cyper_shield_jo/core/constants/app_colors.dart';
import 'package:cyper_shield_jo/core/utils/reponsive_size_helper.dart';
import 'package:flutter/material.dart';

class ReportDetails extends StatelessWidget {
  const ReportDetails({
    super.key,
    required this.containerPadding,
    required this.horizontalMargin,
    required this.spacingHeight,
    required this.textFont,
    required this.bottomSpacing,
    required this.title,
    required this.type,
    required this.percentage,
  });

  final double containerPadding;
  final double horizontalMargin;
  final double spacingHeight;
  final double textFont;
  final double bottomSpacing;
  final String title;
  final String type;
  final String percentage;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(containerPadding),
      margin: EdgeInsets.symmetric(horizontal: horizontalMargin),
      decoration: BoxDecoration(
        color: AppColors.surfaceColor,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.surfaceColor.withOpacity(0.08)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(height: spacingHeight),
          Row(
            children: [
              Icon(Icons.link, color: AppColors.grayColor),
              SizedBox(width: responsiveWidth(context, 12)),

              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      title, // TODO: change this to real domain
                      style: TextStyle(
                        fontSize: textFont,
                        fontWeight: FontWeight.w600,
                        letterSpacing: 0.5,
                        color: AppColors.whiteColor,
                      ),
                      overflow: TextOverflow.ellipsis,
                    ),
                    Text(
                      type,
                      style: TextStyle(
                        color: AppColors.grayColor.withOpacity(0.5),
                        fontSize: textFont - 4,
                      ),
                    ),
                  ],
                ),
              ),

              SizedBox(width: 12),
              Text(
                percentage,
                style: TextStyle(
                  color: AppColors.orangeColor,
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
          SizedBox(height: spacingHeight),
          Container(
            padding: EdgeInsets.symmetric(horizontal: 12, vertical: 4),
            decoration: BoxDecoration(
              color: AppColors.redColor.withOpacity(0.1),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(
                color: AppColors.surfaceColor.withOpacity(0.08),
              ),
            ),
            child: Text("Under Review"),
          ),
          SizedBox(height: bottomSpacing),
        ],
      ),
    );
  }
}
