import 'package:cyper_shield_jo/feature/home_feature/presentation/views/widgets/input_card.dart';
import 'package:flutter/material.dart';

class BuildAnalyzeTab extends StatelessWidget {
  const BuildAnalyzeTab({super.key});

  //! done resposive
  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;

    // the padding of the card(resposive)
    double horizontalPadding = screenWidth < 600 ? 16 : 40;

    // the width of the card
    double maxWidth = screenWidth < 800 ? screenWidth : 600;

    return Padding(
      padding: EdgeInsets.symmetric(horizontal: horizontalPadding),
      child: Center(
        child: ConstrainedBox(
          constraints: BoxConstraints(maxWidth: maxWidth),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: const [InputCard()],
          ),
        ),
      ),
    );
  }
}
