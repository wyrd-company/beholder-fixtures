using Catalog.Web.Logging;
using Catalog.Web.Models;
using Catalog.Web.Services;
using Microsoft.AspNetCore.Mvc;

namespace Catalog.Web.Controllers;

[ApiController]
[Route("api/[controller]")]
public sealed class CatalogController : ControllerBase
{
    private readonly CatalogService _service;
    private readonly ILogger<CatalogController> _logger;

    public CatalogController(CatalogService service, ILogger<CatalogController> logger)
    {
        _service = service;
        _logger = logger;
    }

    [HttpGet("{id:int}")]
    public ActionResult<CatalogEntry> GetById(int id, [FromQuery] string? format)
    {
        var entry = _service.FindById(id);
        if (entry is null)
        {
            return NotFound();
        }

        CatalogLogger.CatalogViewed(_logger, id.ToString(), format ?? "unknown");
        return Ok(entry);
    }

    [HttpGet]
    public ActionResult<IReadOnlyList<CatalogEntry>> List([FromQuery] int? take)
    {
        var all = _service.ListAll();
        if (take.HasValue)
        {
            return Ok(all.Take(take.Value).ToList());
        }

        return Ok(all);
    }

    [HttpPost]
    public ActionResult<CatalogEntry> Create([FromBody] CatalogEntry entry)
    {
        var created = _service.Create(entry);
        return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
    }
}
