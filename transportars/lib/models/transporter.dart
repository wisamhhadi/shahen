class Transporter {
  final int id;
  final String name;
  final String? phone;
  final String? city;
  final String? location;
  final int balance;

  Transporter({required this.id, required this.name, this.phone, this.city, this.location, required this.balance});

  factory Transporter.fromJson(Map<String, dynamic> json) {
    return Transporter(
      id: int.tryParse("${json['id']}") ?? 0,
      name: "${json['name'] ?? 'ناقل'}",
      phone: json['phone']?.toString(),
      city: json['city']?.toString(),
      location: json['location']?.toString(),
      balance: int.tryParse("${json['balance'] ?? 0}") ?? 0,
    );
  }
}
