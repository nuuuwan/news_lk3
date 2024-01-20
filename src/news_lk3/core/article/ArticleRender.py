from functools import cache


class ArticleRender:
    @cache
    def render_continued(self) -> str:
        return '...'

    @cache
    def get_original_body(self, max_chars: int) -> str:
        total_chars = 0
        display_lines = []
        is_partial = False
        for line in self.original_body_lines:
            if len(line) + total_chars > max_chars:
                display_lines.append(self.render_continued())
                is_partial = True
                break
            display_lines.append(line)
            total_chars += len(line)
        if not is_partial:
            display_lines.append('◼️')
        return '\n\n'.join(display_lines)
