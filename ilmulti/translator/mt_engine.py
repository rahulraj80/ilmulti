import ilmulti
def autolog(message):
    "Automatically log the current function details."
    import inspect, logging
    # Get the previous frame in the stack, otherwise it would
    # be this function!!!
    print(">"*10)
    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    #logging.debug("%s: %s in %s:%i" % (
    #    message, 
    #    func.co_name, 
    #    func.co_filename, 
    #    func.co_firstlineno
    #))
    print("%s: %s in %s:%i" % (
        message, 
        func.co_name, 
        func.co_filename, 
        func.co_firstlineno
    ))
    print(">"*10)

class MTEngine:
    def __init__(self, translator, segmenter, tokenizer):
        self.segmenter = segmenter
        self.tokenizer = tokenizer
        self.translator = translator

    def __call__(self, source, tgt_lang, src_lang=None, detokenize=True):
        """
        Uses segmenter -> tokenizer -> translator and lays out the
        interaction.
        """
        lang, lines = self.segmenter(source, lang=src_lang)
        autolog(f"lang:{lang}::Num Lines:{len(lines)}::Lines:{lines}::T:{str(type(lines))}:T0:{str(type(lines[0]))}::Source:{source}:")
        sources = []
        for line in lines:
            lang, tokens = self.tokenizer(line, lang=src_lang)
            src_lang = src_lang or lang
            autolog(f":lang:{src_lang}::Tokens::T:{str(type(tokens))}:Tokens:{tokens}::lango:{lang}:")
            # Unsupervised tokenization.
            tokens = [ilmulti.utils.language_token(tgt_lang)] + tokens
            content = ' '.join(tokens)
            sources.append(content)
            autolog(f":Content::T:{str(type(content))}:content:{content}:::Tokens2::T:{str(type(tokens))}:Tokens2_len:{len(tokens)}::Tokens10:{tokens[:10]}:::")

        autolog(f":Sources::T:{str(type(sources))}:len:{len(sources)}:::Sources::T:{sources}:::")
        export = self.translator(sources)
        export = self._handle_empty_lines_noise(export)
        if detokenize:
            export = self._detokenize(export)
        return export

    def _handle_empty_lines_noise(self, exports):
        _exports = []
        for entry in exports:
            if not entry['src'].strip():
                entry['tgt'] = ''
            _exports.append(entry)
        return _exports


    def _detokenize(self, export):
        _exports = []
        for entry in export:
            for key in ['src', 'tgt']:
                entry[key] = self.tokenizer.detokenize(entry[key])
            entry['src'] = entry['src'][9:]
            _exports.append(entry)
        return _exports
