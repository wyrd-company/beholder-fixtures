library;

class DeferredPayload {
  const DeferredPayload(this.label);

  final String label;
}

const List<DeferredPayload> payloadValues = <DeferredPayload>[
  DeferredPayload('alpha'),
  DeferredPayload('beta'),
];

String describePayload(DeferredPayload payload) => 'payload:${payload.label}';
