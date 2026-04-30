hexo.extend.filter.register('after_post_render', function (data) {
  const cfg = hexo.config.heading_numbering || {};
  if (cfg.enable === false) return data;

  const minLevel = Number(cfg.min_level || 1);
  const maxLevel = Number(cfg.max_level || 6);
  const scope = cfg.scope || 'post';

  if (scope === 'post' && data.layout && data.layout !== 'post') {
    return data;
  }

  if (!data.content) return data;

  const counters = [0, 0, 0, 0, 0, 0];
  const headingRe = /<h([1-6])([^>]*)>([\s\S]*?)<\/h\1>/gi;

  data.content = data.content.replace(headingRe, (full, levelText, attrs = '', inner = '') => {
    const level = Number(levelText);
    if (level < minLevel || level > maxLevel) return full;
    if (/\sdata-heading-numbered=(['"])true\1/i.test(attrs)) return full;
    if (/<span[^>]*class=(['"])[^'"]*\bheading-number\b[^'"]*\1/i.test(inner)) return full;

    const index = level - 1;
    counters[index] += 1;
    for (let i = index + 1; i < counters.length; i += 1) {
      counters[i] = 0;
    }

    const parts = counters.slice(minLevel - 1, index + 1).filter(Boolean);
    if (parts.length === 0) return full;

    // Remove markdown-it generated anchor links from headings.
    const cleanInner = inner.replace(
      /<a\b[^>]*class=(['"])[^'"]*\bheader-anchor\b[^'"]*\1[^>]*>[\s\S]*?<\/a>/i,
      ''
    );

    const prefix = `<span class="heading-number">${parts.join('.')} </span>`;
    return `<h${level}${attrs} data-heading-numbered="true">${prefix}${cleanInner}</h${level}>`;
  });

  return data;
});
