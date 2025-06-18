import pathlib
import attr
from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank import progressbar as pb
from pylexibank import FormSpec


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "leecaijia"

    def cmd_makecldf(self, args):
        # add bib
        args.writer.add_sources()
        args.log.info("added sources")

        corrections = {
                "tsh": "tsʰ",
                "tɕh": "tɕʰ",
                "kh": "kʰ",
                "th": "tʰ",
                "ph": "pʰ",
                }

        # add concept
        concepts = {}
        for concept in self.conceptlists[0].concepts.values():
            idx = concept.id.split("-")[-1] + "_" + slug(concept.english)
            args.writer.add_concept(
                    ID=idx,
                    Name=concept.english,
                    Concepticon_ID=concept.concepticon_id,
                    Concepticon_Gloss=concept.concepticon_gloss
                    )
            concepts[concept.id] = idx
        args.log.info("added concepts")

        # add language
        args.writer.add_language(
                ID="Caijia",
                Glottocode="caij1234",
                Name="Caijia"
                )
        args.log.info("added languages")

        # read in data
        data = self.raw_dir.read_csv(
                "data.tsv", 
                delimiter="\t", dicts=True)
        # extend corrections
        for i, row in enumerate(data):
            form = row["Caijia (segments  separated)"]
            for s, t in zip("12345", "¹²³⁴⁵"):
                form = form.replace(s, t)
            row["Segments"] = [corrections.get(c, c) for c in form.split()]

        # add data
        for entry in data:
            if entry["Id"].strip():
                cid = entry["Id"]
            if entry["Caijia"].strip() != "/":
                args.writer.add_form_with_segments(
                        Language_ID="Caijia",
                        Parameter_ID=concepts[cid],
                        Value=entry["Caijia"],
                        Form=entry["Caijia"],
                        Segments=entry["Segments"],
                        Source="Lee2022"
                        )

