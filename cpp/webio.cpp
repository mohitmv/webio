

namespace webio {
namespace detail {

namespace {



} // namespace

void BuildFrameInternals(FrontEndElement* frame, FrameInternals* internals) {
  int element_index_counter = 0;
  auto lGetUniqueIndex = [&]() {
    element_index_counter += 1;
    return element_index_counter;
  };
  std::function<void(FrontEndElement& frame)> lEvaluateFrameRecursive;
  lEvaluateFrameRecursive = [&](FrontEndElement& frame) {
    frame.element_id = lGetUniqueIndex();
    if (frame.has_options) {
      internals->options[frame.element_id] = frame.options_;
    }
    if (frame.has_id) {
      internals->element_internal_id_to_display_id_map[frame.element_id] = frame.id_;
    }
    if (frame.has_onclick) {
      frame.onclick_id = lGetUniqueIndex();
      internals->registered_actions[frame.onclick_id] = frame.onclick_;
    }
    if (frame.has_onchange) {
      frame.onchange_id = lGetUniqueIndex();
      internals->registered_actions[frame.onchange_id] = frame.onchange_;
    }
    if (frame.has_menu_options) {
      frame.menu_options_onclick_ids.resize(frame.menu_options_.size());
      for (int i = 0; i < frame.menu_options_.size(); i++) {
        int onclick_id = frame.menu_options_onclick_ids[i] = lGetUniqueIndex();
        internals->registered_actions[onclick_id] = frame.menu_options_[i].second;
      }
    }
    for (auto& child_frame : frame.children) {
      lEvaluateFrameRecursive(child_frame);
    }
  };
  lEvaluateFrameRecursive(*frame);
}

namespace helpers {

std::exception ToException(std::exception_ptr eptr) {
  try {
    if (eptr) {
      std::rethrow_exception(eptr);
    }
    return std::exception();
  } catch (const std::exception& e) {
    return e;
  }
}

}  //namespace helpers


void PopulateInputs(
    const Json& input_params,
    const FrameInternals& internals,
    unordered_map<std::string, InputObject>* inputs_objects) {
  auto& e_id_map = internals.element_internal_id_to_display_id_map;
  for (auto& item: input_params.object_items()) {
    int element_id = std::stoi(item.first);
    if (qk::ContainsKey(e_id_map, element_id)) {
      string element_display_id = e_id_map.at(element_id);
      auto& io = (*inputs_objects)[element_display_id];
      if (item.second.is_number()) {  // Must be DropDown.
        io.selected = item.second.int_value();
        io.value = internals.options.at(element_id).at(io.selected);
      } else if(item.second.is_string()) {
        io.value = item.second.string_value();
      } else if (item.second.is_array()) {
        for (auto& item2: item.second.array_items())
        io.selected_list.push_back(item2.int_value());
      } else if (item.second.is_bool()) {
        io.on = item.second.bool_value();
      }
    }
  }
}


}  // namespace details
}