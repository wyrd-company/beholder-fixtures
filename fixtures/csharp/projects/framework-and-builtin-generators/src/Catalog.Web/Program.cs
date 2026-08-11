using Catalog.Web.Logging;
using Catalog.Web.Models;
using Catalog.Web.Serialization;
using Catalog.Web.Services;
using Catalog.Web.Text;
using Microsoft.AspNetCore.Mvc;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddRazorPages();
builder.Services.AddSingleton<CatalogService>();

var app = builder.Build();

app.MapGet("/health", () => Results.Ok(new { status = "ok" }));

app.MapGet("/catalog/{id:int}", GetCatalogById);

app.MapGet("/catalog/code/{code}", (string code) =>
{
    var isValid = CatalogPatterns.IsValidCatalogCode(code);
    return isValid ? Results.Ok(new { code, valid = true }) : Results.BadRequest(new { code, valid = false });
});

app.MapPost("/catalog", ([FromBody] CatalogEntry entry, CatalogService service, ILogger<Program> logger) =>
{
    CatalogLogger.EntryCreated(logger, entry.Id, entry.Name);
    var created = service.Create(entry);
    return Results.Created($"/catalog/{created.Id}", created);
});

app.MapGet("/catalog/json/{catalogId}", (string catalogId, CatalogService service) =>
{
    var envelope = service.BuildEnvelope(catalogId);
    var generated = CatalogJsonService.SerializeWithContext(envelope);
    var reflected = CatalogJsonService.SerializeWithReflection(envelope);
    return Results.Ok(new { generated, reflected });
});

app.MapControllers();
app.MapRazorPages();

app.Run();

static IResult GetCatalogById(int id, CatalogService service)
{
    var entry = service.FindById(id);
    return entry is null ? Results.NotFound() : Results.Ok(entry);
}

public partial class Program
{
}
