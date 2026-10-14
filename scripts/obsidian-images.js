hexo.extend.filter.register('before_post_render', function (data) {
  if (!data.content) return data;

  // Convert Obsidian image embeds to Markdown, preserving spaces in URLs.
  data.content = data.content.replace(
    /^([ \t]*)!\[\[(\/?img\/[^\]\r\n]+)\]\]([ \t]*)$/gm,
    (match, indent, imagePath, trailing) =>
      `${indent}![](<${imagePath.startsWith('/') ? imagePath : '/' + imagePath}>)${trailing}`
  );

  data.content = data.content.replace(
    /(!\[[^\]\n]*\]\()img\//g,
    '$1/img/'
  );
  return data;
});
