import 'package:flutter/material.dart';
import 'screens/loan_application_screen.dart';
import 'screens/loan_status_screen.dart';

void main() {
  runApp(const BankLoanApp());
}

class BankLoanApp extends StatelessWidget {
  const BankLoanApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Bank Loan App',
      theme: ThemeData(primarySwatch: Colors.blue),
      initialRoute: '/',
      routes: {
        '/': (context) => const LoanApplicationScreen(),
        '/loan_status': (context) {
          final loanId = ModalRoute.of(context)!.settings.arguments as String;
          return LoanStatusScreen(loanId: loanId);
        },
      },
    );
  }
}
