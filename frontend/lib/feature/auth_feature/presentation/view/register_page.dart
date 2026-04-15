import 'package:cyper_shield_jo/core/utils/reponsive_size_helper.dart';
import 'package:cyper_shield_jo/core/widgets/logo.dart';
import 'package:cyper_shield_jo/feature/auth_feature/presentation/view/login_page.dart';
import 'package:cyper_shield_jo/feature/auth_feature/presentation/view/widgets/text_field.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:cyper_shield_jo/core/constants/app_colors.dart';

class RegisterPage extends StatefulWidget {
  const RegisterPage({super.key});

  @override
  State<RegisterPage> createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();
  final FirebaseAuth auth = FirebaseAuth.instance;

  @override
  void dispose() {
    emailController.dispose();
    passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.backgroundColor,
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 20),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Logo(),
              const SizedBox(height: 40),
              Text(
                "Please enter your email to verify your account",
                style: TextStyle(color: AppColors.whiteColor, fontSize: 15),
              ),
              const SizedBox(height: 40),
              TextFields(
                emailController: emailController,
                label: "Email",
                icon: Icons.email,
              ),
              const SizedBox(height: 20),
              TextFields(
                emailController: passwordController,
                label: "Password",
                icon: Icons.lock,
              ),
              const SizedBox(height: 30),
              ElevatedButton(
                onPressed: () {
                  final email = emailController.text.trim();
                  final password = passwordController.text.trim();
                  if (email.isEmpty && !email.contains('@')) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Please enter your email')),
                    );
                  } else if (password.isEmpty || password.length < 8) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(
                        content: Text('Please enter your password'),
                      ),
                    );
                  } else {
                    //TODO: implement login logic(verify Email)
                    Navigator.pushReplacement(
                      context,
                      MaterialPageRoute(builder: (context) => LoginPage()),
                    );

                    // _sendSignInLink(email);
                  }
                },
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(
                    vertical: 15,
                    horizontal: 100,
                  ),
                  backgroundColor: AppColors.primaryColor,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                child: const Text(
                  'Register',
                  style: TextStyle(fontSize: 18, color: Colors.white),
                ),
              ),
              SizedBox(height: responsiveHeight(context, 16)),
              RichText(
                text: TextSpan(
                  text: "Already have an account? ",
                  style: TextStyle(color: AppColors.whiteColor, fontSize: 15),
                  children: [
                    TextSpan(
                      text: "Login",
                      style: TextStyle(
                        color: AppColors.primaryColor,
                        fontSize: 15,
                      ),
                      recognizer: TapGestureRecognizer()
                        ..onTap = () {
                          Navigator.pushReplacement(
                            context,
                            MaterialPageRoute(
                              builder: (context) => LoginPage(),
                            ),
                          );
                        },
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
