class TransportOrder {
  final int id;
  final String title;
  final String? fromName;
  final String? toName;
  final String? captainName;
  final String? captainStatus;

  TransportOrder({required this.id, required this.title, this.fromName, this.toName, this.captainName, this.captainStatus});

  factory TransportOrder.fromJson(Map<String, dynamic> json) => TransportOrder(
        id: int.tryParse("${json['id']}") ?? 0,
        title: "${json['collection_area'] ?? 'طلب شحن'}",
        fromName: json['from_name']?.toString(),
        toName: json['to_name']?.toString(),
        captainName: json['captain_name']?.toString(),
        captainStatus: json['captain_status']?.toString(),
      );
}
